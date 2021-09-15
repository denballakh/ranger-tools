/** @file */
struct TGalaxy {
    VMT cls;

    _gap_32 _004;
    _gap_32 _008;
    _gap_32 _00C;
    _gap_32 _010;
    _gap_32 _014;
    _gap_32 _018;
    int id_ship;                        ///< ID последнего созданного корабля
    _gap_32 _020;
    _gap_32 _024;
    int player_index;                   ///< номер игрока в списке рейнджеров
    TList* stars;                       ///< список звезд
    TList* holes;                       ///< список черных дыр
    TList* _034;                        ///< список ?
    TList* planets;                     ///< список планет
    TList* rangers;                     ///< список рейнджеров
    int pirate_cnt;                     ///< кол-во пиратов
    _gap_32 _044;
    int _048;
    int turn;                           ///< текущий ход
    byte diff_levels[8];                ///< сложности партии
    int32_t gen_seed;                   ///< сид генерации галактики
    int32_t rnd_seed;                   ///< сид рандома
    int rangers_average_capital;        ///< средний капитал рейнджеров
    int _064;
    float rangers_average_strength;     ///< средняя сила рейнджеров
    int _06C;
    _gap_32 _070;
    _gap_32 _074;
    int eminent_rangers[3];             ///< три самых лучших рейнджера?
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
    TList* planet_news;                 ///< список новостей
    TList* custom_weapon_infos;
    TStar* keller_attack_star;          ///< цель атаки Келлера
    TList* _0C0;
    TList* _0C4;
    TDomResearchProgress dom_researches[3]; ///< прогресс исследований доминаторских программ
    float _0EC;  // 0.01
    byte GTL;                           ///< ГТУ
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
    int terron_weapon_lock_turn;        ///< ход
    int terron_grow_lock_turn;          ///< ход
    int terron_landing_lock_turn;       ///< ход
    int terron_to_star;                 ///< ход
    int keller_leave;                   ///< ход
    int keller_new_research;            ///< ход
    int blazer_landing;                 ///< ход
    int blazer_self_destruction;        ///< ход
    int terron_turn_win;                ///< ход
    int keller_turn_win;                ///< ход
    int blazer_turn_win;                ///< ход
    int pirate_win_turn;                ///< ход
    int pirate_win_type;                ///< ход
    int coalition_defeated_turn;        ///< ход
    _gap_32 _14C;
    TList* scripts;                     ///< список всех скриптов (в том числе и неактивных?)
    TList* _154;
    TList* _158;
    TList* _15C;
    _gap_32 _160;
    TList* constellations;              ///< список секторов
    _gap_32 _168;
    PTR _16C;  // указатель на массив элементов размером 0x60
    _gap_32 _170;
    _gap_32 _174;
    _gap_32 _178;
    _gap_32 _17C;  // сет читов?
    _gap _180;
    _gap _181;
    bool zawarudo;                      ///< флаг от чита ZAWARUDO
    byte _183;
    STR _184;

    // Тонкие настройки:
    bool AA_enabled;                    ///< флаг тонких настроек
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
    TList* events;                      ///< список галактических событий
    TList* interface_state_overrides;   ///< список оверрайдов состояния
    TList* interface_text_overrides;    ///< список оверрайдов текста
    TList* interface_image_overrides;   ///< список оверрайдов изображения
    TList* interface_pos_overrides;     ///< список оверрайдов позиции
    TList* interface_size_overrides;    ///< список оверрайдов размера
    _gap_32 _1C8;
    _gap_32 _1CC;  // CRC
    byte _1D0;
    _gap _1D1;
    _gap _1D2;
    _gap _1D3;
};
