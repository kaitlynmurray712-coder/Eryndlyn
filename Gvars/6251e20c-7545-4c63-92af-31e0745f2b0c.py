# ===================================================
# tool_check module 
# 2023-08-23: Updated tool_name_for to return tool_key (instead of throwing error) in case the key is not found in the tool dictionary
# 2023-06-09: Updated ensure_compatibility to handle rogue commas in pTools and eTools
# 2022-09-21: Only checks abilities for the purpose of detemining JoAT discrepancy
# 2022-09-07: Support Tools Dict Extension per Server
# 2022-08-31: Initial Version
# ===================================================

CUSTOM_DICT_SVAR = 'toolDictionary'
CUSTOM_DICT_GVAR_ADDRESS = 'toolDictionaryGvar'
CUSTOM_TOOLS_CVAR = 'customTools'
CUSTOM_TOOL_CHECK_ABILITIES = 'customToolCheckAbilities'

TOOLS_DICT_EXTENSION_SVAR = 'toolExtension'

DEFAULT_TOOLS_DICT_GVAR = 'e65831da-1834-4089-9bbd-93fc36a2d622'
PROF_CVAR = 'toolProficiencies'
PROF_DISPLAY_CVAR = 'pTools'
EXPR_DISPLAY_CVAR = 'eTools'

# ALL_TOOLS_DICT
base_tools_dict = {}
if get_svar(CUSTOM_DICT_SVAR):
    base_tools_dict = load_yaml(get_svar(CUSTOM_DICT_SVAR))
elif get_svar(CUSTOM_DICT_GVAR_ADDRESS):
    base_tools_dict = load_yaml(get_gvar(get_svar(CUSTOM_DICT_GVAR_ADDRESS)))
else:
    base_tools_dict = load_yaml(get_gvar(DEFAULT_TOOLS_DICT_GVAR))
# Add Extension
if get_svar(TOOLS_DICT_EXTENSION_SVAR):
    server_tools_extension = load_yaml(get_svar(TOOLS_DICT_EXTENSION_SVAR))
    for server_tool in server_tools_extension.keys():
        base_tools_dict[server_tool] = server_tools_extension[server_tool]

ALL_TOOLS_DICT = base_tools_dict

if character().get_cvar(CUSTOM_TOOLS_CVAR):
    custom_tools = load_yaml(character().get_cvar(CUSTOM_TOOLS_CVAR))
    for tool in custom_tools:
        ALL_TOOLS_DICT[tool] = custom_tools[tool]

ALL_TOOLS_DICT_KEYS = ALL_TOOLS_DICT.keys()

ABILITIES_MAP = {
    'str': 'strength',
    'dex': 'dexterity',
    'con': 'constitution',
    'int': 'intelligence',
    'wis': 'wisdom',
    'cha': 'charisma'
}

# ==============
# DATA STRUCTURE
# ==============

# `tool` object (yaml)
#
# smithstools:
#   key: smithstools
#   name: "Smith's Tools"
#   type: artisan
#   abilities:
#     - strength
#     - dexterity

# =======
# METHODS
# =======
# use .doc to get the docstring
#
# MAIN METHODS
# - matching_tools
# - tool_check_dice_str
#
# DISPLAY
# - embed_tool_fields
#
# UTILITY
# - keyify
# - exact_tool
# - tool_name_for
# - tool_type_for
# - tool_abilities_for
# 
# TOOL PROFICIENCY
# - char_proficiencies
# - is_proficient
# - tool_proficiency
# - joat
# - joat_discrepancy
# - reliable_talent
# - best_ability
# - tool_proficiency_str
# 
# COMPATIBILITY
# - ensure_compatibility
# - overwrite_display_cvars

def keyify(input_str):
    """keyify(input_str)
    => returns:     valid tool_key str for the given full name of the tool
    => rtype:       str"""
    output_str = input_str.lower()
    to_replace = [' ', "'", "’", "-", ',']
    for sym in to_replace:
        output_str = output_str.replace(sym, '')
    return output_str

def matching_tools(search_str):
    """matching_tools(str)
    => returns:     a list of tool keys matching the given (sub)string.
    => rtype: list
    => Example:     matching_tools('thi') => ['thievestools']"""

    user_tool_key = keyify(search_str)
    exact_match = user_tool_key in ALL_TOOLS_DICT_KEYS
    if exact_match:
        return [user_tool_key]

    user_tool_matches = []
  
    for tool_key in ALL_TOOLS_DICT_KEYS:
        if user_tool_key in tool_key:
            user_tool_matches.append(tool_key)
    return user_tool_matches

def exact_tool(tool_key):
    """exact_tool(tool_key)
    => returns:     matching tool
    => rtype:       `tool`
    """
    return ALL_TOOLS_DICT[tool_key]

def tool_name_for(tool_key):
    """tool_name_for(tool_key)
    => rtype:       str
    """
    if ALL_TOOLS_DICT.get(tool_key):
        return ALL_TOOLS_DICT[tool_key].name
    else:
        return tool_key

def tool_type_for(tool_key):
    """tool_type_for(tool_key)
    => rtype:       str
    """
    return ALL_TOOLS_DICT[tool_key].type

def tool_abilities_for(tool_key):
    """tool_abilities_for(tool_key)
    => returns:     a list of abilities for the tool. Can be overriden with customToolCheckAbilities cvar.
    => rtype:       list
    """
    if character().get_cvar(CUSTOM_TOOL_CHECK_ABILITIES):
        custom_abilities = load_yaml(character().get_cvar(CUSTOM_TOOL_CHECK_ABILITIES))
        if tool_key in custom_abilities.keys():
            return [custom_abilities[tool_key]]
    return ALL_TOOLS_DICT[tool_key].abilities

def char_proficiencies():
    """char_proficiencies()
    => returns:     a dictionary of the current character's proficiencies.
                    proficiency = 1
                    expertise = 2
    => rtype:       dict"""
    return load_yaml(character().get_cvar(PROF_CVAR, default={}))

def is_proficient(tool_key):
    """is_proficient(tool_key)
    => returns:     whether the current character has proficiency in the tool.
    => rtype:       boolean"""
    return tool_key in char_proficiencies().keys()

def tool_proficiency(tool_key):
    """tool_proficiency(tool_key)
    => returns:     an integer representing the proficiency; 0: not proficient, 1: proficient, 2: expertise
    => rtype:       int"""
    if not is_proficient(tool_key):
        return 0
    return char_proficiencies()[tool_key]

def joat():
    """joat()
    => returns:     whether the character has Jack of All Trades class feature
    => rtype:       boolean"""
    return any(skill[1].prof == 0.5 for skill in character().skills)

def joat_discrepancy():
    """joat_discrepancy()
    => returns:     whether the base ability checks don't have half proficiency included.
    => rtype:       boolean"""
    half_prof_missing = any(skill[1].prof == 0 for skill in character().skills if skill[0] in ABILITIES_MAP.values())
    return joat() and half_prof_missing

def reliable_talent(tool_key):
    """reliable_talent(tool_key)
    => returns:     whether Reliable Talent applies to the given tool
    => rtype:       boolean"""
    return is_proficient(tool_key) and character().csettings['talent']

def best_ability(tool_key):
    """best_ability(tool_key)
    => returns:     name of the best ability to use.
    => rtype:       str, or None if no default ability list for the tool exists."""
    default_abilities = tool_abilities_for(tool_key)
    if default_abilities == []:
        return None
    char_best_ability = None
    char_best_ability_name = ''
    for abil in default_abilities:
        char_abil = character().skills[abil]
        if (not char_best_ability) or (char_abil.value > char_best_ability.value):
            char_best_ability = char_abil
            char_best_ability_name = abil
    if not char_best_ability:
        return None
    return char_best_ability_name

def tool_proficiency_str(tool_key):
    """tool_proficiency_str(tool_key)
    Handles proficiency, expertise, and Jack of All Trades.
    => returns:     proficiency bonus string for the given tool. 
    => rtype:       str, or None if there is no tool proficiency"""
    half_prof_missing = joat_discrepancy()
    half_prof_bonus = floor(character().stats.prof_bonus/2)
    if not is_proficient(tool_key):
        half_prof_bonus_text = half_prof_bonus + "[JoAT]"
        return half_prof_bonus_text if half_prof_missing else None
    prof_int = tool_proficiency(tool_key)
    prof_type_str = ['', 'proficient', 'expertise'][prof_int]
    char_prof_bonus = character().stats.prof_bonus
    prof_bonus = char_prof_bonus * prof_int
    if joat() and (not half_prof_missing):
        prof_bonus -= floor(char_prof_bonus/2)
        prof_type_str = '(after JoAT) ' + prof_type_str
    return f'{prof_bonus}[{prof_type_str}]'

# =============
# COMPATIBILITY
# =============
def ensure_compatibility():
    """Internal function to ensure compatibility with the old tool alias. Loads from pTools and eTools cvars and saves to toolProficiency cvar"""
    proficiencies = char_proficiencies()
    prof_display = character().get_cvar(PROF_DISPLAY_CVAR, default='')
    expr_display = character().get_cvar(EXPR_DISPLAY_CVAR, default='')
    
    prof_displays = [] if prof_display == '' else prof_display.split(', ')
    expr_displays = [] if expr_display == '' else expr_display.split(', ')
        
    # Do nothing if they are synced
    display_dict = {}
    for item in prof_displays:
        item_key = keyify(item)
        if item_key != '':   
            display_dict[item_key] = 1
    for item in expr_displays:
        item_key = keyify(item)
        if item_key != '':
            display_dict[item_key] = 2
    if display_dict == proficiencies:
        return None

    # Sync
    proficiencies = display_dict
    character().set_cvar(PROF_CVAR, dump_yaml(proficiencies))

def overwrite_display_cvars():
    """Overwrites pTools and eTools cvar with information in toolProficiency cvar"""
    proficiencies = char_proficiencies()
    prof_keys = proficiencies.keys()
    prof_displays = [tool_name_for(key) for key in prof_keys if proficiencies[key] == 1]
    expr_displays = [tool_name_for(key) for key in prof_keys if proficiencies[key] == 2]
    character().set_cvar(PROF_DISPLAY_CVAR, ', '.join(prof_displays))
    character().set_cvar(EXPR_DISPLAY_CVAR, ', '.join(expr_displays))

# =======
# DISPLAY
# =======
def embed_tool_fields():
    """Returns a string of Proficiencies and Expertise fields to be used for embeds"""
    ensure_compatibility()
    profs = character().get_cvar(PROF_DISPLAY_CVAR, default='').replace(', ', "\n")
    exps = character().get_cvar(EXPR_DISPLAY_CVAR, default='').replace(', ', "\n")
    return f''' -f "Proficient|{'None' if profs == '' else profs}" -f "Expertise|{'None' if exps == '' else exps}" '''

# =============
# Main Function
# =============

def tool_check_dice_str(tool_key, ability_override=None, base_adv=None, reroll=None, min_val=None, mod_override=None):
    """tool_check_dice_str(tool_key, ability_override=None, base_adv=None, reroll=None, min_val=None, mod_override=None)
    > tool_key (str):           Use matching_tools() to search for the valid key
    > ability_override (str):   [strength/dexterity/constitution/intelligence/wisdom/charsma]
    > base_adv (bool):          Whether this roll should be made at adv (True), dis (False), or normally (None).
    > reroll (int):             If the roll lands on this number, reroll it once. The function already handles Halfling Luck racefeat.
    > min_val (int):            The minimum value of the dice roll. The function already handles Reliable Talent
    > mod_override(int):        Overrides the skill modifier.
    
    => returns:                 a dice string for the given tool_key
    => rtype:                   str, or None if default ability doesn't exist for the tool. ability_override is required in this case."""
    ensure_compatibility()
    ability_for_check = ability_override if ability_override else best_ability(tool_key)
    if not ability_for_check:
        return 'd20'
    
    reroll = reroll if reroll else character().csettings['reroll']
    reliable_min = 10 if reliable_talent(tool_key) else None
    min_val = min_val if min_val else reliable_min

    base_dice_str = character().skills[ability_for_check].d20(base_adv=base_adv, reroll=reroll, min_val=min_val, mod_override=mod_override)
    tool_proficiency = tool_proficiency_str(tool_key)
    result_dice_str = base_dice_str + f'+{tool_proficiency}' if tool_proficiency else base_dice_str
    return  result_dice_str