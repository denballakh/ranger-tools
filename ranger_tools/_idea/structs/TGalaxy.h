struct TGalaxy {
    __cls* cls;

    _gap_32 _004;
    _gap_32 _008;
    _gap_32 _00C;
    _gap_32 _010;
    _gap_32 _014;
    _gap_32 _018;
    int id_ship;
    _gap_32 _020;
    _gap_32 _024;
    int player_index;  // номер игрока в списке рейнджеров
    TList* stars;
    TList* holes;
    TList* _034;
    TList* planets;
    TList* rangers;
    TList* RC_list;
    _gap_32 _044;
    int _048;
    int turn;
    byte diff_levels[8];
    int rnd;
    int rnd_out;
    int rangers_average_capital;
    int _064;
    float rangers_average_strength;
    int _06C;
    _gap_32 _070;
    _gap_32 _074;
    int eminent_rangers[3];
    _gap_32 _084;
    _gap_32 _088;
    _gap_32 _08C;
    _gap_32 _090;
    _gap_32 _094;
    _gap_32 _098;
    _gap_32 _09C;
    _gap_32 _0A0;
    _gap_32 _0A4;
    _gap_32 _0A8;
    _gap_32 _0AC;
    _gap_32 _0B0;
    _gap_32 _0B4;
    _gap_32 _0B8;
    _gap_32 _0BC;
    TList* planet_news;
    TList* custom_weapon_infos;
    TStar* keller_attack_star;
    TList* _0C0;
    TList* _0C4;
    TDomResearchProgress dom_researches[3];
    float _0EC;  // 0.01
    byte GTL;
    _gap _0F1;
    _gap _0F2;
    _gap _0F3;
    int _0F8;
    int _0FC;
    int _0FD;

    int _100;
    int _104;
    int _108;
    int _10C;
    int _110;
    int terron_weapon_lock_turn;
    int terron_grow_lock_turn;
    int terron_landing_lock_turn;
    int terron_to_star;
    int keller_leave;
    int keller_new_research;
    int blazer_landing;
    int blazer_self_destruction;
    int terron_turn_win;
    int keller_turn_win;
    int blazer_turn_win;
    int pirate_win_turn;
    int pirate_win_type;
    int coalition_defeated_turn;
    _gap_32 _14C;
    TList* scripts;
    TList* _154;
    TList* _158;
    TList* _15C;
    _gap_32 _160;
    TList* constellations;
    _gap_32 _168;
    PTR _16C;  // указатель на массив элементов размером 0x60
    _gap_32 _170;
    _gap_32 _174;
    _gap_32 _178;
    _gap_32 _17C;  // сет читов?
    _gap _180;
    _gap _181;
    bool zawarudo;
    byte _183;
    STR _184;

    // Тонкие настройки:
    bool AA_enabled;
    byte AA_kling_strength;
    byte AA_kling_aggro;
    byte AA_kling_spawn;
    byte AA_pirate_aggro;
    byte AA_coal_aggro;
    byte AA_asteroid_mod;
    byte AA_sun_damage_mod;
    byte AA_extra_inventions;
    byte AA_akrin_mod;
    byte AA_node_drop_mod;
    byte AA_AB_drop_value_mod;
    byte AA_drop_value_mod;
    byte AA_ag_planets;
    byte AA_mi_planets;
    byte AA_in_planets;
    byte AA_extra_rangers;
    byte AA_AB_hitpoints_mod;
    byte AA_AB_damage_mod;
    byte AA_AI_tolerate_junk;
    byte AA_rnd_chaotic;
    byte AA_eq_knowledge_restricted;
    byte AA_ruins_near_stars;
    byte AA_ruins_targetting_full;
    byte AA_special_ships_in_game;
    byte AA_zero_start_exp;
    byte AA_AB_battle_royale;
    byte AA_kling_racial_weapons;
    byte AA_start_center;
    byte AA_max_range_missiles;
    byte AA_old_hyper;
    byte AA_pirate_nodes;
    byte AA_AI_use_shops;
    byte AA_ruins_use_shops;
    byte AA_duplicate_arts;
    byte AA_hull_growth;

    // FCustomRules: boolean;

    // FCustomKlingStr: byte;
    // FCustomKlingAggro: byte;
    // FCustomKlingSpawn: byte;
    // FCustomPirateAggro:byte;
    // FCustomCoalAggro: byte;
    // FCustomAsteroidMod:byte;
    // FCustomSunDamageMod:byte;
    // FCustomExtraInventions: byte;
    // FCustomAkrinMod: byte;

    // FCustomNodeDropMod: byte;
    // FCustomABDropValueMod: byte;
    // FCustomDropValueMod: byte;
    // FCustomAgPlanets: byte;
    // FCustomMiPlanets: byte;
    // FCustomInPlanets: byte;
    // FCustomExtraRangers: byte;
    // FCustomABHitpointsMod: byte;
    // FCustomABDamageMod: byte;
    // FCustomAITolerateJunk: byte;

    // FCustomRuleRnd: boolean;
    // FCustomRuleTechKnowledge: boolean;
    // FCustomRuleRuinsPos: boolean;
    // FCustomRuleRuinsTargetting: boolean;
    // FCustomRuleSpecilShips:boolean;

    // FCustomRuleZeroExp: boolean;
    // FCustomRuleABattleRoyale: boolean;
    // FCustomRuleKlingRacialWeapons: boolean;
    // FCustomRuleStartCenter: boolean;
    // FCustomRuleMaxRangeMissiles: boolean;

    // FCustomRuleOldHyper: boolean;
    // FCustomRulePirateNodes: boolean;

    // FCustomRuleAIBuysEqFromShops: boolean;
    // FCustomRuleRuinsUsingShop: boolean;
    // FCustomRuleDuplicateArtsAllowed:boolean;

    // FCustomRuleHullGrowth:byte;

    _gap_32 _1AC;
    TList* events;
    TList* interface_state_overrides;
    TList* interface_text_overrides;
    TList* interface_image_overrides;
    TList* interface_pos_overrides;
    TList* interface_size_overrides;
    _gap_32 _1C8;
    _gap_32 _1CC;  // CRC
    byte _1D0;
    _gap _1D1;
    _gap _1D2;
    _gap _1D3;
};
