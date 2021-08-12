struct TDomResearchProgress {
    int progress;
    int speed;
    /*
        speed:
        0 - 200
        1 - 100
        2 - 70
        3 - 30
        4 - 0
    */
};

struct TGalaxy {
    __cls* cls;

    _gap_32 _004;
    _gap_32 _008;
    _gap_32 _00C;
    _gap_32 _010;
    _gap_32 _014;
    _gap_32 _018;
    _gap_32 _01C;
    _gap_32 _020;
    _gap_32 _024;
    _gap_32 _028;
    TList* stars;
    TList* holes;
    _gap_32 _034;
    TList* planets;
    TList* rangers;
    TList* RC_list;
    _gap_32 _044;
    int _048;
    int turn;
    byte diff_levels[8];
    _gap_32 _058; // rnd_date_based? связано с защитой? кол-во чит очков?
    int rnd_seed;
    _gap_32 _060;
    _gap_32 _064;
    _gap_32 _068;
    _gap_32 _06C;
    _gap_32 _070;
    _gap_32 _074;
    _gap_32 _078;
    _gap_32 _07C;
    _gap_32 _080;
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
    int _0D0;
    TStar* keller_attack_star;
    TDomResearchProgress dom_researches[3];
    // float _0EC; // 0.01
    byte GTL;
    _gap _0F1;
    _gap _0F2;
    _gap _0F3;
    int _0F4;
    int _0F8;
    int _0FC;

    int _100;
    int _104;
    int _108;
    int _10C;
    int _110;
    _gap_32 _114;
    _gap_32 _118;
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
    _gap_32 _150;
    _gap_32 _154;
    _gap_32 _158;
    _gap_32 _15C;
    _gap_32 _160;
    TList* constellations;
    _gap_32 _168;
    _gap_32 _16C;
    _gap_32 _170;
    _gap_32 _174;
    _gap_32 _178;
    _gap_32 _17C; // сет читов
    _gap _180;
    _gap _181;
    bool zawarudo;
    byte _183;
    STR _184;

    // Тонкие настройки:
    bool AA_188_enabled;
    byte AA_189_kling_strength;
    byte AA_18A_kling_aggro;
    byte AA_18B_kling_spawn;
    byte AA_18C_pirate_aggro;
    byte AA_18D_coal_aggro;
    byte AA_18E_asteroid_mod;
    byte AA_18F_sun_damage_mod;
    byte AA_190_extra_inventions;
    byte AA_191_akrin_mod;
    byte AA_192_node_drop_mod;
    byte AA_193_AB_drop_value_drop_mod;
    byte AA_194_drop_value_mod;
    byte AA_195_ag_planets;
    byte AA_196_mi_planets;
    byte AA_197_in_planets;
    byte AA_198_extra_rangers;
    byte AA_199_AB_hitpoints_mod;
    byte AA_19A_AB_damage_mod;
    byte AA_19B_AI_tolerate_junk;
    byte AA_19C_rnd_chaotic;
    byte AA_19D_eq_knowledge_restricted;
    byte AA_19E_ruins_near_stars;
    byte AA_19F_ruins_targetting_full;
    byte AA_1A0_special_ships_in_game;
    byte AA_1A1_zero_start_exp;
    byte AA_1A2_AB_battle_royale;
    byte AA_1A3_kling_racial_weapons;
    byte AA_1A4_start_center;
    byte AA_1A5_max_range_missiles;
    byte AA_1A6_old_hyper;
    byte AA_1A7_pirate_nodes;
    byte AA_1A8_AI_use_shops;
    byte AA_1A9_ruins_use_shops;
    byte AA_1AA_duplicate_arts;
    byte AA_1AB_hull_growth;

    _gap_32 _1AC;
    TList* events;
    _gap_32 _1B4;
    _gap_32 _1B8;
    _gap_32 _1BC;
    _gap_32 _1C0;
    _gap_32 _1C4;
    _gap_32 _1C8;
    _gap_32 _1CC; // CRC
    byte _1D0;
    _gap _1D1;
    _gap _1D2;
    _gap _1D3;
}; // 1D4
