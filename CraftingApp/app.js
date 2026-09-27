const DEFAULT_DATA = {
};

const FIELDS = ["rarity", "tool", "base", "focus", "item1", "item2", "item3", "item4"];

let data = {};
let selectedKey = null;
let originalData = null;

const $ = (id) => document.getElementById(id);

function deepCopy(value) {
  return JSON.parse(JSON.stringify(value));
}

function showToast(message) {
  const toast = $("toast");
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => toast.classList.remove("show"), 2200);
}

function setData(next) {
  data = next;
  renderList();
  if (selectedKey && Object.prototype.hasOwnProperty.call(data, selectedKey)) {
    populateEditor(selectedKey);
  } else {
    selectedKey = null;
    showEmpty();
  }
}

function renderList() {
  const query = $("search").value.trim().toLowerCase();
  const list = $("recipe-list");
  list.innerHTML = "";

  const keys = Object.keys(data)
    .filter(key => key.toLowerCase().includes(query))
    .sort((a, b) => a.localeCompare(b));

  $("recipe-count").textContent = `${Object.keys(data).length}`;

  if (!keys.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.style.margin = "25px 5px";
    empty.innerHTML = "<p>No recipes found.</p>";
    list.appendChild(empty);
    return;
  }

  for (const key of keys) {
    const button = document.createElement("button");
    button.className = "recipe-item" + (key === selectedKey ? " selected" : "");
    button.type = "button";
    button.innerHTML = `
      <span class="recipe-name"></span>
      <span class="recipe-rarity"></span>
    `;
    button.querySelector(".recipe-name").textContent = key;
    button.querySelector(".recipe-rarity").textContent = data[key]?.rarity || "";
    button.addEventListener("click", () => selectRecipe(key));
    list.appendChild(button);
  }
}

function selectRecipe(key) {
  selectedKey = key;
  populateEditor(key);
  renderList();
}

function populateEditor(key) {
  $("empty-state").classList.add("hidden");
  $("editor").classList.remove("hidden");

  const recipe = data[key];
  $("editor-title").textContent = key;
  $("recipe-name").value = key;

  for (const field of FIELDS) {
    $(field).value = recipe?.[field] ?? "";
  }

  $("status").textContent = "Changes are held in memory only.";
}

function showEmpty() {
  $("empty-state").classList.remove("hidden");
  $("editor").classList.add("hidden");
}

function readEditor() {
  const name = $("recipe-name").value.trim();
  const recipe = {};

  for (const field of FIELDS) {
    recipe[field] = $(field).value;
  }

  return { name, recipe };
}

$("editor").addEventListener("submit", (event) => {
  event.preventDefault();

  const { name, recipe } = readEditor();

  // removing unnecessary fields
  for (const field of FIELDS) {
    if (!recipe[field]) {
      delete recipe[field];
    }
  }

  if (!name) {
    showToast("Recipe name is required.");
    $("recipe-name").focus();
    return;
  }

  if (name !== selectedKey && Object.prototype.hasOwnProperty.call(data, name)) {
    showToast("A recipe with that name already exists.");
    return;
  }

  const oldKey = selectedKey;
  if (oldKey && oldKey !== name) {
    delete data[oldKey];
  }

  data[name] = recipe;
  selectedKey = name;

  renderList();
  populateEditor(name);
  $("status").textContent = "Saved in memory. Copy the JSON to export it.";
  showToast("Recipe saved.");
});

$("new-recipe").addEventListener("click", () => {
  const baseName = "new recipe";
  let name = baseName;
  let n = 2;
  while (Object.prototype.hasOwnProperty.call(data, name)) {
    name = `${baseName} ${n++}`;
  }

  data[name] = {
    rarity: "",
    tool: "",
    base: "",
    focus: "",
    item1: "",
    item2: "",
    item3: "",
    item4: ""
  };

  selectedKey = name;
  renderList();
  populateEditor(name);
  $("recipe-name").focus();
  $("recipe-name").select();
});

$("delete-entry").addEventListener("click", () => {
  if (!selectedKey) return;

  const confirmed = confirm(`Delete "${selectedKey}" from the working copy?`);
  if (!confirmed) return;

  delete data[selectedKey];
  selectedKey = null;
  renderList();
  showEmpty();
  showToast("Recipe deleted from the working copy.");
});

$("copy-entry").addEventListener("click", async () => {
  if (!selectedKey) return;

  const entry = { [selectedKey]: data[selectedKey] };
  await copyText(JSON.stringify(entry, null, 4), "Recipe copied to clipboard.");
});

$("copy-all").addEventListener("click", async () => {
  await copyText(JSON.stringify(data, null, 4), "Full JSON copied to clipboard.");
});

async function copyText(text, successMessage) {
  try {
    await navigator.clipboard.writeText(text);
    showToast(successMessage);
  } catch (error) {
    // Fallback for browsers/environments where Clipboard API is unavailable.
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();

    try {
      document.execCommand("copy");
      showToast(successMessage);
    } catch {
      showToast("Could not access the clipboard. Copy the JSON manually.");
    } finally {
      textarea.remove();
    }
  }
}

$("search").addEventListener("input", renderList);

$("reset").addEventListener("click", () => {
  data = deepCopy(originalData);
  selectedKey = null;
  renderList();
  showEmpty();
  showToast("Working copy reset.");
});

$("json-file").addEventListener("change", async (event) => {
  const file = event.target.files?.[0];
  if (!file) return;

  try {
    const text = await file.text();
    const parsed = JSON.parse(text);

    if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") {
      throw new Error("The JSON root must be an object.");
    }

    originalData = deepCopy(parsed);
    data = deepCopy(parsed);
    selectedKey = null;
    renderList();
    showEmpty();
    showToast(`Loaded ${Object.keys(data).length} recipes.`);
  } catch (error) {
    showToast(`Could not load JSON: ${error.message}`);
  } finally {
    event.target.value = "";
  }
});

async function loadCraftingJson() {
  try {

    const response = await fetch("crafting.json", { cache: "no-store" });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const parsed = await response.json();
    if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") {
      throw new Error("The JSON root must be an object.");
    }

    originalData = deepCopy(parsed);
    data = deepCopy(parsed);
    renderList();
  } catch (error) {
    // A static file cannot always be fetched when index.html is opened via file://.
    // The built-in data keeps the interface usable; "Load JSON" can also be used.
    originalData = deepCopy(DEFAULT_DATA);
    data = deepCopy(DEFAULT_DATA);
    renderList();
    showToast("Using built-in sample data. Run from a local server to auto-load crafting.json.");
  }
}

// async function loadCraftingJson() {
//   try {

//     // const response = await fetch("crafting.json", { cache: "no-store" });
//     // load from all_crafting_jsons folder: 0.json -> 10.json

//     for( let i = 0; i < 12; i++) {
//       const response = await fetch(`./all_crafting_jsons/${i}.json`, { cache: "no-store" });
//           if (!response.ok) throw new Error(`HTTP ${response.status}`);

//       const parsed = await response.json();
//       if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") {
//         throw new Error("The JSON root must be an object.");
//       }
//       // update originalData & data
//       originalData = { ...originalData, ...parsed }; //deepCopy(parsed);
//       data = { ...data, ...parsed }; //deepCopy(parsed);
//     }


//     renderList();
//   } catch (error) {
//     // A static file cannot always be fetched when index.html is opened via file://.
//     // The built-in data keeps the interface usable; "Load JSON" can also be used.
//     originalData = deepCopy(DEFAULT_DATA);
//     data = deepCopy(DEFAULT_DATA);
//     renderList();
//     showToast("Using built-in sample data. Run from a local server to auto-load crafting.json.");
//   }
// }

loadCraftingJson();
