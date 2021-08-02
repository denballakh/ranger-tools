#include "sr2_scripter.h"
//#include <QtCore/QCoreApplication>
//#include <QDir>
//#include <QLibrary>
// #include <alloc.h>

// system


long __stdcall FunManager(const long fnum, const long par1, const long par2, const long par3, const long par4) //FunManager@20
{   long val=0;       //long i=0;
    switch (fnum){
        case 0:
        char (*aaa);aaa="abc";
        *(char*)par1=*(aaa+2);

        //*(char*)par1=*("abc"+1);

        //char (*aaa[4]);
        //aaa=(char*)par1;
        //*aaa="abc";
        //*(char*)par1=**aaa;

        //typedef void(*pointer)(void); /* обьявление указателя */
        //pointer fun = (pointer)par1;//&function; fooptr = (int*)a[i]; //*(long*)Addr
        //fun();
        break;

        case 1: val=ReadByte(par1); break;
        case 2: val=WriteByte(par1,par2); break;
        case 3: val=ReadLong(par1); break;
        case 4: val=WriteLong(par1,par2); break;
        case 5: val=ReadFloat(par1); break;
        case 6: val=WriteFloat(par1,par2); break;
        case 7: val=ReadDouble(par1); break;
        case 8: val=WriteDouble(par1,par2); break;

        case 9: val=CreateEmptyList(par1); break;
        case 10: val=CreateGameObject(par1); break;
        case 11: val=AddObjectToList(par1,par2); break;
        case 12: val=RemoveObjectFromList(par1,par2); break;
        case 13: val=FreeGameObject(par1); break;
        case 14: val=CreateEmptyString(par1); break;

 //-------------------------

        case 20: val=DataAddr(); break;
        case 21: val=GalaxyData(par1,par2); break;
        case 22: val=ResearchData(par1,par2,par3); break;
        case 23: val=DiffData(par1,par2); break;

  //------------------------

        case 30: val=IdToSector(par1); break;
        case 31: val=StarToSector(par1); break;
        case 32: val=SectorsNearSector(par1,par2); break;
        case 33: val=SectorData(par1,par2,par3); break;

  //------------------------
        case 40: val=GalaxyStars(par1); break;
        case 41: val=SectorStars(par1,par2); break;
        case 42: val=PlanetToStar(par1); break;
        case 43: val=ShipToStar(par1); break;
        case 44: val=StarData(par1,par2,par3); break;

  //------------------------

        case 50: val=GalaxyHoles(); break;
        case 51: val=HoleData(par1,par2,par3); break;

  //------------------------

        case 60: val=GalaxyPlanets(par1); break;
        case 61: val=StarPlanets(par1,par2); break;
        case 62: val=PlanetData(par1,par2,par3); break;
        case 63: val=PlanetTechProgress(par1,par2,par3); break;

  //------------------------

        case 70: val=StarAsteroids(par1,par2); break;
        case 71: val=AsteroidData(par1,par2,par3); break;

  //------------------------

        case 80: val=StarMissiles(par1,par2); break;
        case 81: val=MissileData(par1,par2,par3); break;

  //------------------------

        case 90: val=StarItems(par1,par2); break;
        case 91: val=PlanetItems(par1,par2); break;
        case 92: val=ShopItems(par1,par2); break;
        case 93: val=ShipItems(par1,par2); break;
        case 94: val=ShipArts(par1,par2); break;
        case 95: val=ShipEqItems(par1,par2); break;
        case 96: val=ShipEqArts(par1,par2); break;

        case 97: val=GeneralItemProperty(par1,par2,par3); break;
        case 98: val=GeneralEqProperty(par1,par2,par3); break;
        case 99: val=EqHullProperty(par1,par2,par3); break;
        case 100: val=EqFuelTankProperty(par1,par2,par3); break;
        case 101: val=EqEngineProperty(par1,par2,par3); break;
        case 102: val=EqRadarProperty(par1,par2); break;
        case 103: val=EqScanerProperty(par1,par2); break;
        case 104: val=EqDroidProperty(par1,par2); break;
        case 105: val=EqHookProperty(par1,par2,par3); break;
        case 106: val=EqDefGenProperty(par1,par2); break;
        case 107: val=EqWeaponProperty(par1,par2,par3); break;
        case 108: val=SatelliteProperty(par1,par2,par3); break;
        case 109: val=CisternProperty(par1,par2,par3); break;
        case 110: val=ItemNodesCount(par1,par2); break;
        case 111: val=ItemGoodsCount(par1,par2); break;
        case 112: val=BeaconCharge(par1,par2); break;
        case 113: val=UselessDummyFunction(); break;
        case 114: val=TrancToShip(par1); break;

        case 115: val=ItemCreate(par1,par2,par3,par4); break;
        case 116: val=GetItemFromShip(par1,par2); break;
        case 117: val=GetArtFromShip(par1,par2); break;
        case 118: val=PutItemInShip(par1,par2); break;
        case 119: val=GetItemFromShop(par1,par2); break;
        case 120: val=PutItemInShop(par1,par2); break;
        case 121: val=DigItemFromPlanet(par1,par2); break;
        case 122: val=HideItemOnPlanet(par1,par2,par3,par4); break;

    //------------------------
        case 130: val=Distance(par1,par2); break;
        case 131: val=CoordX(par1,par2); break;
        case 132: val=CoordY(par1,par2); break;
    //------------------------
        //case 140: val=Player(); break;
        case 140: val=PlayerPrograms(par1,par2); break;
    //------------------------
        case 150: val=GalaxyShips(par1,par2); break;
        case 151: val=GalaxyRangers(par1); break;
        case 152: val=StarShips(par1,par2); break;
        case 153: val=PlanetMilitary(par1,par2); break;

        case 154: val=ShipStats(par1,par2,par3); break;
        case 155: val=ShipSkillsData(par1,par2,par3,par4); break;
        case 156: val=HealthFactor(par1,par2,par3); break;
        case 157: val=ClearHealthFactor(par1,par2); break;
        case 158: val=AddHealthFactor(par1,par2,par3,par4); break;
        case 159: val=ShipMedals(par1,par2); break;
        case 160: val=ShipMedalChange(par1,par2,par3); break;
        case 161: val=ShipAddMedal(par1,par2); break;
        case 162: val=ShipRemoveMedal(par1,par2); break;
        case 163: val=ShipCountDuplicateMedals(par1,par2); break;
        case 164: val=ShipSetSkin(par1,par2,par3); break;
        case 165: val=ShipHaveArt(par1,par2); break;
        case 166: val=ShipHaveArtEquipped(par1,par2); break;
        case 167: val=RepairShipEq(par1,par2,par3); break;
        case 168: val=DamageShipEq(par1,par2,par3); break;
        case 169: val=ShipMissileAmmoCheck(par1,par2); break;
        case 170: val=ShipMissileAmmoChange(par1,par2); break;
        case 171: val=ShipMass(par1); break;
        case 172: val=ShipFreeSpace(par1); break;

        case 180: val=ShipFlightPlan(par1,par2,par3); break;
        case 181: val=OrderMove(par1,par2,par3); break;
        case 182: val=OrderLand(par1,par2); break;
        case 183: val=OrderEnterHole(par1,par2); break;
        case 184: val=OrderLiftOff(par1); break;
        case 185: val=OrderStop(par1); break;
        case 186: val=OrderFollow(par1,par2); break;
        case 187: val=OrderAggroFollow(par1,par2); break;
        case 188: val=OrderAttack(par1,par2,par3); break;



    //------------------------

        };
    return val;}

//---------------------------------system----------------------------

byte __stdcall ReadByte(const long Addr) //ReadByte@4 //1
{ return *(byte*)Addr;}

byte __stdcall WriteByte(const long Addr, const byte Value) //WriteByte@8 //2
{byte i=*(byte*)Addr;
 *(byte*)Addr=Value;
   return i;}

long __stdcall ReadLong(const long Addr) //ReadLong@4 //3
{return *(long*)Addr;}

long __stdcall WriteLong(const long Addr, const long Value) //WriteLong@8 //4
{long i=*(long*)Addr;
 *(long*)Addr=Value;
   return i;}

long __stdcall ReadFloat(const long Addr) //ReadFloat@4 //5
{float i=*(float*)Addr;
 if (i>127*256*256*256) {i=127*256*256*256;}
 if (i<-127*256*256*256) {i=-127*256*256*256;}
 long i2=i;
 return i2;}

long __stdcall WriteFloat(const long Addr, const float Value) //WriteFloat@8 //6
{float i=*(float*)Addr;
 if (i>127*256*256*256) {i=127*256*256*256;}
 if (i<-127*256*256*256) {i=-127*256*256*256;}
 *(float*)Addr=Value;
 long i2=i;
 return i2;}

long __stdcall ReadDouble(const long Addr) //ReadDouble@4 //7
{double i=*(double*)Addr;
 if (i>127*256*256*256) {i=127*256*256*256;}
 if (i<-127*256*256*256) {i=-127*256*256*256;}
 long i2=i;
 return i2;}

long __stdcall WriteDouble(const long Addr, const double Value) //WriteDouble@8 //8
{double i=*(double*)Addr;
 *(double*)Addr=Value;
 if (i>127*256*256*256) {i=127*256*256*256;}
 if (i<-127*256*256*256) {i=-127*256*256*256;}
 long i2=i;
 return i2;}


long __stdcall CreateGameObject(const long size) //CreateGameObject@4 //9
{long val=4+(long)malloc(size+10); long i=0;
 if (val>4) {WriteLong(val-4,size+6);
     WriteLong(val+size,6);
     while (i<size) { WriteByte(val+i,0); i=i+1;}}
return val;}

long __stdcall CreateEmptyList(const long listtype) //CreateEmptyList@4 //10
{long val=CreateGameObject(16);
 long temp=CreateGameObject(5*4);
 WriteLong(val,listtype);
 WriteLong(val+4,temp);
 WriteLong(val+8,0);
 WriteLong(val+12,5);
return val;}


long __stdcall AddObjectToList(const long list,const long obj) //AddObjectToList@8 //11
{long val=0; long i=0;
 long numitems=ReadLong(list+8);
 long maxitems=ReadLong(list+12);
 long oldlist=ReadLong(list+4);
 if (numitems==maxitems){
 long newlist=CreateGameObject(4*(numitems+5));
     if (newlist>4) {
        WriteLong(newlist-4,4*(numitems+5)+6);
        WriteLong(newlist+4*(numitems+5),6);
        while (i<numitems*4) {WriteLong(newlist+i,ReadLong(oldlist+i));i=i+4;}
        if (oldlist>0) {FreeGameObject(oldlist);}
        WriteLong(list+4,newlist);
        WriteLong(list+12,maxitems+5);
        maxitems=maxitems+5;
        oldlist=newlist;  }}
 if (numitems<maxitems) {
 WriteLong(oldlist+4*numitems,obj);
 WriteLong(list+8,numitems+1);
 val=1;} //success
 return val;}


long __stdcall RemoveObjectFromList(const long list,const long objnum) //RemoveObjectFromList@8 //12
{long val=0; long i=0;
 long numitems=ReadLong(list+8);
 long adrlist=ReadLong(list+4);
 if (((numitems+1)>objnum) and (objnum>0)){
     val=ReadLong(adrlist+4*(objnum-1));
     WriteLong(list+8,numitems-1);
     i=objnum;
     while (i<numitems){WriteLong(adrlist+4*(i-1),ReadLong(adrlist+4*i));i=i+1;}}
 return val;}


long __stdcall FreeGameObject(const long obj) //FreeGameObject@4 //13
{if (obj>0) {free((void*)obj);}
 return 0;}

long __stdcall CreateEmptyString(const long size) //CreateEmptyString@4 //14
{long memsize=2*size; if ((size%2)>0) {memsize=memsize+2;} //size - in symbols
    long val=4+(long)malloc(memsize+8); long i=0;
 if (val>4) {WriteLong(val-4,size*2);
     while (i<memsize) { WriteByte(val+i,0); i=i+1;}}
return val;}


//---------------------------------galaxy----------------------------

long __stdcall DataAddr() //DataAddr@0 //20
{long i=ReadLong(7362768);
long i2=ReadLong(i);
return i2;}

long __stdcall GalaxyData(const long property, const long value) //GalaxyData@8 //21
{long val=0;
    switch (property){
                     case 1: //GameDate
                     val=ReadLong(DataAddr()+72);
                     if (value>0) {WriteLong(DataAddr()+72,value);}
                     break;

                     // пока все, потом сюда добавится еще функционал

                    }
return val;}


long __stdcall ResearchData(const long subrace,const long type, const long value) //ResearchData@12 //22
{long val=0; long adr=DataAddr()+196;
    if ((subrace>-1) and (subrace<3)) {
        if (type==0) { //percent
            val=ReadFloat(adr+8*subrace);
            if ((value>-1) and (value<101)){WriteFloat(adr+8*subrace,value);}}
        if (type==1)  { //material
        val=ReadLong(adr+4+8*subrace);
        if (value>-1) {WriteLong(adr+4+8*subrace,value);}}}
    if (type==2) { //galaxy tech level
    val=ReadByte(adr+28);
    //if ((value>0) and (value<9)) {WriteByte(adr+28,value);} //нет смысла изменять, пересчитывается каждый ход
    }
    return val;} //subrace - 0-Blazer,1-Keller,2-Terron

long __stdcall DiffData(const long type, const long value) //DiffData@8 //23
{long val=0; long adr=DataAddr()+75;
    if ((type>0) and (type<9)) {
        val=1+ReadByte(adr+type);
        if ((value>0) and (value<5)) {WriteByte(adr+type,value-1);}}
    return val;} //type: 1..8 - Dominators,Prices,Science,Breaks,Equipment,Tasks,Holes,Luck
                // value 1..5 (0 - только посмотреть)


//-------------------------------sectors-----------------------------------------------

long __stdcall IdToSector(const long id) //IdToSector@4 //30
{long val=0; long i=0;
long sectorlist=ReadLong(DataAddr()+296);
long seccount=ReadLong(sectorlist+8);
val=seccount;
if ((id>0) and (id<seccount+1)) {
    val=ReadLong(ReadLong(sectorlist+4)+(id-1)*4);
    while ((i<seccount) and (!(ReadLong(val+4)==id))) {val=ReadLong(ReadLong(sectorlist+4)+i*4);i=i+1;}} //если вдруг сектора не по порядку
return val;}


long __stdcall StarToSector(const long star) //StarToSector@4 //31
{return ReadLong(ReadLong(star+180)+4);} //возвращает Id, не адрес


long __stdcall SectorsNearSector(const long sector, const long num) //SectorsNearSector@8 //32
{long val=0; long secadr=sector; if (secadr<100) {secadr=IdToSector(secadr);} //принимает и адрес и Id
long seclist=ReadLong(secadr+28);
long seccount=ReadLong(seclist+8);
val=seccount;
if ((num>0) and (num<seccount+1)) {val=ReadLong(ReadLong(ReadLong(seclist+4)+(num-1)*4)+4);}
return val;} //возвращает Id одного из соседних секторов или их количество



long __stdcall SectorData(const long sector, const long property, const long value) //SectorData@12 //33
{long val=0; long adr=sector; if (adr<100) {adr=IdToSector(adr);} //принимает и адрес и Id
    switch (property){
                     case 1: //Id
                     val=ReadFloat(adr + 4);
                     break;
                     case 2: //Open/Closed
                     val=ReadByte(adr + 9);
                     if (value>-1) {WriteByte(adr + 9,value);}; // 1,0
                     break;

                     // пока все, потом сюда добавится еще функционал

                    }
return val;}


//-------------------------------stars-----------------------------------------------


long __stdcall GalaxyStars(const long starid) //GalaxyStars@4 //40
{long val=0;long i=0;
long starlist=ReadLong(DataAddr()+44);
long starscount=ReadLong(starlist+8);
val=starscount;
if ((starid>0) and (starid<starscount+1)) {val=ReadLong(ReadLong(starlist+4)+(starid-1)*4);
  while ((i<starscount) and (!(ReadLong(val+4)==starid))) {val=ReadLong(ReadLong(starlist+4)+i*4);i=i+1;}} //если вдруг звезды не по порядку}
return val;}


long __stdcall SectorStars(const long sector, const long num) //SectorStars@8 //41
{long val=0; long secadr=sector; if (secadr<100) {secadr=IdToSector(secadr);} //принимает и адрес и Id
long starlist=ReadLong(secadr+24);
long starcount=ReadLong(starlist+8);
val=starcount;
if ((num>0) and (num<starcount+1)) {val=ReadLong(ReadLong(starlist+4)+(num-1)*4);}
return val;}


long __stdcall PlanetToStar(const long planet) //PlanetToStar@4 //42
{return ReadLong(planet+24);}

long __stdcall ShipToStar(const long ship) //PlanetToStar@4 //43
{return ReadLong(ship+32);}


long __stdcall StarData(const long star, const long property, const long value) //StarData@12 //44
{   long val=0;
    switch (property){
                     case 1: //DamageRadius
                     val=ReadFloat(star + 80);
                     if (value>-1) {WriteFloat(star + 80,value);};
                     break;
                     case 2: //ThreatRadius
                     val=ReadFloat(star + 76);
                     if (value>-1) {WriteFloat(star + 76,value);};
                     break;

                     // пока все, потом сюда добавится еще функционал

                    }
    return val;}


//-----------------------------holes--------------------------------------------------------

long __stdcall GalaxyHoles() //GalaxyHoles@0 //50
{return ReadLong(ReadLong(DataAddr()+48)+8);}

long __stdcall HoleData(const long num, const long property, const long value) //HoleData@12 //51
{   long i=GalaxyHoles();
    long val=0;
    if ((num<i+1) and (num>0) and (property>0) and (property<4)) {
                    long adr=ReadLong(ReadLong(ReadLong(DataAddr()+48)+4) + (num-1)*4);
                    val=ReadLong(adr + property*12 - 4);
                    if (value>0) {WriteLong(adr + property*12 - 4,value);}
    }; //property: 1-in star, 2-to star, 3-closing date
    return val;}

//-------------------------------------planets------------------------------------------------------



long __stdcall GalaxyPlanets(const long planetnum) // GalaxyPlanets@4 //60
{long val=0;
long planetscount=ReadLong(ReadLong(DataAddr()+52)+8);
if ((planetnum>0) and (planetnum<planetscount+1)) {val=ReadLong(ReadLong(ReadLong(DataAddr()+52)+4)+(planetnum-1)*4);}
if (planetnum==0) {val=planetscount;}
return val;} // num=ID


long __stdcall StarPlanets(const long Star, const long num) //StarPlanets@8 //61
{   long i=ReadLong(Star+40);
    long count=ReadLong(i+8);
    long val=0;
    if ((num>0) and (num<count+1)) {val=ReadLong(ReadLong(i + 4) + 4*(num-1));}
    if (num==0) {val=count;}
    return val;}


long __stdcall PlanetData(const long planet, const long property, const long value) //PlanetData@12 //62
{   long val=0;
    switch (property){
                     case 1: //population
                     val=ReadLong(planet + 116);
                     if (value>-1) {WriteLong(planet + 116,value);};
                     break;
                     case 2: //economy
                     val=ReadByte(planet + 120);
                     if ((value>-1) and (value<3)) {WriteByte(planet + 120,value);};
                     break;
                     case 3: //cur race (при значении = 6-незаселенная) //если сделать незаселенной изначально (т.е. с начала игры) обитаемую планету - при посадке будет вылет - поскольку картинка не загрузится
                     val=ReadByte(planet + 128);
                     if ((value>-1) and (value<7)) {WriteByte(planet + 128,value);};
                     break;
                     case 4: //race
                     val=ReadByte(planet + 130);
                     if ((value>-1) and (value<5)) {WriteByte(planet + 130,value);};
                     break;
                     case 5: //government
                     val=ReadByte(planet + 131);
                     if ((value>-1) and (value<5)) {WriteByte(planet + 131,value);};
                     break;

                     // добавить данные о разведке, орбите
                    }
    return val;}

//planet tech progress
long __stdcall PlanetTechProgress(const long planet, const long property, const long value) //PlanetTechProgress@12 //63
{   long val=0;
    switch (property){
                     case 1: //tech level
                     val=ReadByte(planet + 79);
                     if ((value>0) and (value<9)) {WriteByte(planet + 79,value);};
                     break;

                     // ---
                    }
    return val;}



//--------------------------------------asteroids-----------------------------------------------------


long __stdcall StarAsteroids(const long Star, const long num) //PlanetInStar@8 //70
{   long val=0;
    long i=ReadLong(Star+44);
    if (i>0) {long count=ReadLong(i+8);
    val=count;
    if ((num>0) and (num<count+1)) {val=ReadLong(ReadLong(i + 4) + 4*(num-1));}}
    return val;}



long __stdcall AsteroidData(const long asteroid, const long property, const long value) //AsteroidData@12 //71
{   long val=0;
    switch (property){
                     case 1: //Id
                     val=ReadLong(asteroid + 4);
                     break;
                     case 2: //Minerals
                     val=ReadLong(asteroid + 48);
                     if (value>-1) {WriteLong(asteroid + 48,value);};
                     break;

                     // пока все, потом сюда добавится еще функционал

                    }
    return val;}


//-------------------------------------missiles------------------------------------------------------


long __stdcall StarMissiles(const long Star, const long num) //StarMissiles@8 //80
{   long val=0;
    long i=ReadLong(Star+60);
    if (i>0) {long count=ReadLong(i+8);
    val=count;
    if ((num>0) and (num<count+1)) {val=ReadLong(ReadLong(i + 4) + 4*(num-1));}}
    return val;}



long __stdcall MissileData(const long missile, const long property, const long value) //MissileData@12 //81
{   long val=0;
    switch (property){
                     case 1: //Id
                     val=ReadLong(missile + 8);
                     break;
                     case 2: //missile(50)/torpedo(61)
                     val=ReadByte(missile + 12);
                     if (value>0) {WriteByte(missile + 12,value);};
                     break;
                     case 3: //tech level
                     val=ReadByte(missile + 13);
                     if (value>0) {WriteByte(missile + 13,value);};
                     break;
                     case 4: //mindamage
                     val=ReadByte(missile + 14);
                     if (value>-1) {WriteByte(missile + 14,value);};
                     break;
                     case 5: //maxdamage
                     val=ReadByte(missile + 15);
                     if (value>-1) {WriteByte(missile + 15,value);};
                     break;
                     case 6: //owner (ship address)
                     val=ReadLong(missile + 36);
                     if (value>0) {WriteLong(missile + 36,value);};
                     break;
                     case 7: //target (obj address)
                     val=ReadLong(missile + 40);
                     if (value>0) {WriteLong(missile + 40,value);};
                     break;

                     // пока все, потом сюда добавится еще функционал

                    }
    return val;}


//-------------------------------------items------------------------------------------------------

long __stdcall StarItems(const long Star, const long num) //StarItems@8 //90
{   long i=ReadLong(Star+52);
    long count=ReadLong(i+8);
    long val=count;
    if ((num>0) and (num<count+1)) {val=ReadLong(ReadLong(i + 4) + 4*(num-1));}
    return val;}

long __stdcall PlanetItems(const long planet, const long num) //PlanetItems@8 //91
{   long i=ReadLong(planet+348);
    long count=ReadLong(i+8);
    long val=count;
    if ((num>0) and (num<count+1)) {val=ReadLong(12+ReadLong(ReadLong(i + 4) + 4*(num-1)));}
    return val;}

long __stdcall ShopItems(const long obj, const long num) //ShopItems@8 //92
{   long val=0; //obj - планета или база
    long objheader=ReadLong(obj);
    if ((objheader==6465444) or (objheader==5276056) or (objheader==5282716) or (objheader==5289956)
        or (objheader==5297104) or (objheader==5304092) or (objheader==5310656)) {
    long ofs=956;
    if (objheader==6465444) {ofs=292;}
    long i=ReadLong(obj+ofs);
    long count=ReadLong(i+8);
    val=count;
    if ((num>0) and (num<count+1)) {val=ReadLong(ReadLong(i + 4) + 4*(num-1));}}
    return val;}

long __stdcall ShipItems(const long ship, const long num) //ShipItems@8 //93
{   long i=ReadLong(ship+732);
    long count=ReadLong(i+8);
    long val=count;
    if ((num>0) and (num<count+1)) {val=ReadLong(ReadLong(i + 4) + 4*(num-1));}
    return val;}

long __stdcall ShipArts(const long ship, const long num) //ShipArts@8 //94
{   long i=ReadLong(ship+736);
    long count=ReadLong(i+8);
    long val=count;
    if ((num>0) and (num<count+1)) {val=ReadLong(ReadLong(i + 4) + 4*(num-1));}
    return val;}


long __stdcall ShipEqItems(const long ship, const long eqtype) //ShipEqItems@8 //95
{   long val=0;
    if ((eqtype>0) and (eqtype<14)) {val=ReadLong(ship+236+eqtype*4);}
return val;} //eqtype =  1..13 ,hull,fueltank,engine,radar,scaner,droid,hook,defgen,weapon1..5


long __stdcall ShipEqArts(const long ship, const long slot) //ShipEqArts@8 //96
{   long val=0; long artcount=ShipArts(ship,0); long i=0; long artadr=0;
    if ((slot>0) and (slot<5)) {
      while (i<artcount) {i=i+1;artadr=ShipArts(ship,i); if (ReadByte(artadr+68)==slot){val=artadr;i=artcount;}}}
return val;} //artslot =  1..4




long __stdcall GeneralItemProperty(const long item, const long property, const long value) //GeneralItemProperty@12 //97
{long val=0;
if (item>0) {
long itemtype=ReadLong(item+12);
switch (property){
        case 1: //type
        val=itemtype;
        break;
        case 2: //item ID
        val=ReadLong(item+8);
        break;
        case 3: //size
        val=ReadLong(item+24);
        if (not(value==0)) {WriteLong(item+24,value);} // оставлена возможность сделать отрицательный размер; чтобы просто считать размер - value=0
        break;
        case 4: //race
        val=ReadByte(item+28);
        if ((value>0) and (value<7) and not((itemtype==39) and ((value==5) or (value>6)))) {WriteByte(item+28,value);}
        break;
        case 5: //subrace
            if (itemtype>8) {val=ReadByte(item+74);
                if ((value>-1) and (value<3)) {WriteByte(item+74,value);}}
        break;
        case 6: //price
        val=ReadLong(item+32);
        if (not(value==0)) {WriteLong(item+32,value);} // оставлена возможность сделать отрицательную цену; чтобы просто считать цену - value=0
        break;}}

return val;}


long __stdcall GeneralEqProperty(const long item, const long property, const long value) //GeneralEqProperty@12 //98
{long val=0;
if (item>0) {
long itemtype=ReadLong(item+12);
switch (property){
        case 1: //techlevel
            if (itemtype==39){val=ReadByte(item+84);
                if ((value>0) and (value<9)) {WriteByte(item+84,value);}}
            else {val=ReadByte(item+80);
                if ((value>0) and (value<9)) {WriteByte(item+80,value);}}
        break;
        case 2: //module
        val=ReadByte(item+72);
        if (value>-1) {WriteByte(item+72,value);}
        break;
        case 3: //unimod
        val=ReadByte(item+73);
        if (value>-1) {WriteByte(item+73,value);}
        break;
        case 4: //condition , для корпуса берем оставшееся HP
        if (itemtype==39){val=ReadLong(item+80);
                          if (value>0) {WriteLong(item+80,value);}}
        else {val=ReadDouble(item+56);
              if (value>-1) {WriteDouble(item+56,value);}};
        break;
        case 5: //broken
            if (!(itemtype==39)) {val=ReadLong(item+64);
                if (value>-1) {WriteLong(item+64,value);}}
        break;
        case 6: //in use
        val=ReadLong(item+52);
        break;}}
return val;}

long __stdcall EqHullProperty(const long item, const long property, const long value) //EqHullProperty@12 //99
{long val=0;
if (item>0) {
if (ReadLong(item+12)==39){
switch (property){
        case 1: //броня
        val=ReadByte(item+85);
        if (value>-1) {WriteByte(item+85,value);}
        break;
        case 2: //тип корпуса
        val=ReadByte(item+86);
        if (value>-1) {WriteByte(item+86,value);}
        break;
        case 3: //серия
        val=ReadByte(item+87);
        if (value>-1) {WriteByte(item+87,value);}
        break;
    }}}
return val;}

long __stdcall EqFuelTankProperty(const long item, const long property, const long value) //EqFuelTankProperty@12 //100
{long val=0;
if (item>0) {
if (ReadLong(item+12)==40){
switch (property){
        case 1: //fuel
        val=ReadLong(item+84);
        if (value>-1) {WriteLong(item+84,value);}
        break;
        case 2: //capacity
        val=ReadLong(item+88);
        if (value>-1) {WriteLong(item+88,value);}
        break;
    }}}
return val;}

long __stdcall EqEngineProperty(const long item, const long property, const long value) //EqEngineProperty@12 //101
{long val=0;
if (item>0) {
if (ReadLong(item+12)==41){
switch (property){
        case 1: //speed
        val=ReadLong(item+84);
        if (value>-1) {WriteLong(item+84,value);}
        break;
        case 2: //jump
        val=ReadByte(item+88);
        if (value>-1) {WriteByte(item+88,value);}
        break;
        case 3: //overheat
        val=ReadByte(item+89);
        if (value>-1) {WriteByte(item+89,value);}
        break;
    }}}
return val;}

long __stdcall EqRadarProperty(const long item, const long value) //EqRadarProperty@8 //102
{long val=0;
if (item>0) {
if (ReadLong(item+12)==42){ //range
        val=ReadLong(item+84);
        if (value>-1) {WriteLong(item+84,value);}
    }}
return val;}

long __stdcall EqScanerProperty(const long item, const long value) //EqScanerProperty@8 //103
{long val=0;
if (item>0) {
if (ReadLong(item+12)==43){ //power
        val=ReadByte(item+81);
        if (value>-1) {WriteByte(item+81,value);}
    }}
return val;}

long __stdcall EqDroidProperty(const long item, const long value) //EqDroidProperty@8 //104
{long val=0;
if (item>0) {
if (ReadLong(item+12)==44){ //repair
        val=ReadByte(item+81);
        if (value>-1) {WriteByte(item+81,value);}
    }}
return val;}


long __stdcall EqHookProperty(const long item, const long property, const long value) //EqHookProperty@12 //105
{long val=0;
if (item>0) {
if (ReadLong(item+12)==45){
switch (property){
        case 1: //power
        val=ReadLong(item+84);
        if (value>-1) {WriteLong(item+84,value);}
        break;
        case 2: //range
        val=ReadLong(item+88);
        if (value>-1) {WriteLong(item+88,value);}
        break;
        case 3: //speed1
        val=ReadFloat(item+92);
        if (value>-1) {WriteFloat(item+92,value);}
        break;
        case 4: //speed2
        val=ReadFloat(item+96);
        if (value>-1) {WriteFloat(item+96,value);}
        break;
    }}}
return val;}

long __stdcall EqDefGenProperty(const long item, const long value) //EqDefGenProperty@8 //106
{long val=0;
if (item>0) {
if (ReadLong(item+12)==46){ //power
        val=100-100*ReadFloat(item+84);
        if (value>-1) {WriteFloat(item+84,1-value*0.01);}
    }}
return val;}


long __stdcall EqWeaponProperty(const long item, const long property, const long value) //EqWeaponProperty@12 //107
{long val=0;
if (item>0) {
if ((ReadLong(item+12)>46) and (ReadLong(item+12)<62)){
switch (property){
        case 1: //range
        val=ReadLong(item+84);
        if (value>-1) {WriteLong(item+84,value);}
        break;
        case 2: //minatt //работает, просто не показывается
        val=ReadByte(item+88);
        if (value>-1) {WriteByte(item+88,value);}
        break;
        case 3: //maxatt
        val=ReadByte(item+89);
        if (value>-1) {WriteByte(item+89,value);}
        break;
        case 4: //missile
        val=ReadLong(item+100);
        if (value>-1) {WriteLong(item+100,value);}
        break;
        case 5: //missile max
        val=ReadLong(item+104);
        if (value>-1) {WriteLong(item+104,value);}
        break;
    }}}
return val;}


long __stdcall SatelliteProperty(const long item, const long property, const long value) //SatelliteProperty@12 //108
{long val=0;
if (item>0) {
if (ReadLong(item+12)==66){
       switch (property){
        case 1: //level
        val=ReadByte(item+80);
        if (value>-1) {WriteByte(item+80,value);}
        break;
        case 2: //water
        val=ReadByte(item+96);
        if (value>-1) {WriteByte(item+96,value);}
        break;
        case 3: //land
        val=ReadByte(item+97);
        if (value>-1) {WriteByte(item+97,value);}
        break;
        case 4: //hills
        val=ReadByte(item+98);
        if (value>-1) {WriteByte(item+98,value);}
        break;
    }}}
return val;}

long __stdcall CisternProperty(const long item, const long property, const long value) //CisternProperty@12 //109
{long val=0;
if (item>0) {
if (ReadLong(item+12)==65){
switch (property){
        case 1: //fuel
        val=ReadByte(item+80);
        if (value>-1) {WriteByte(item+80,value);}
        break;
        case 2: //capacity
        val=ReadByte(item+84);
        if (value>-1) {WriteByte(item+84,value);}
        break;
    }}}
return val;}


long __stdcall ItemNodesCount(const long item, const long value) //ItemNodesCount@8 //110
{long val=0;
if (item>0) {
if (ReadLong(item+12)==62){
        val=ReadLong(item+80);
        if (value>-1) {WriteLong(item+80,value);}}}
return val;}


long __stdcall ItemGoodsCount(const long item, const long value) //ItemNodesCount@8 //111
{long val=0;
if (item>0) {
if (ReadLong(item+12)<8){
        val=ReadLong(item+52);
        if (value>-1) {WriteLong(item+52,value);}}}
return val;}

long __stdcall BeaconCharge(const long item, const long value) //ItemNodesCount@8 //112
{long val=0;
if (item>0) {
if (ReadLong(item+12)==22){
        val=ReadLong(item+80);
        if (value>-1) {WriteLong(item+80,value);}}}
return val;}


long __stdcall UselessDummyFunction() //  //113
{long val=0;
//if (item>0) {}
return val;}
//useless item type


long __stdcall TrancToShip(const long item) //TrancToShip@4 //114
{long val=0;
    if (item>0) {if (ReadLong(item)==6815744){val=ReadLong(item+80);}}
    return val;}


long __stdcall ItemCreate(const long type, const long race, const long level, const long size) //ItemCreate@16 //115
{long val=0; long header=0; long datasize=0; long i=0;

    //arts
    if ((type>8) and (type<20)) {header=6813444+(type-9)*152;}
    if (type==20) {header=6815120;}
    if (type==21) {header=6815276;}
    if (type==22) {header=6815432;}
    if (type==23) {header=6815592;}
    if ((type>24) and (type<39)) {header=6815904+(type-25)*152;}
    if (type==32) {header=6816964;}
    if ((type>8) and (type<39)) {datasize=80;}
    if (type==22) {datasize=84;} //beacon


    //eq
    if (type==39) {header=6810904; datasize=88;} //hull
    if (type==40) {header=6811048; datasize=92;} //fueltank
    if (type==41) {header=6811196; datasize=92;} //engine
    if (type==42) {header=6811340; datasize=88;} //radar
    if (type==43) {header=6811484; datasize=84;} //scaner
    if (type==44) {header=6811628; datasize=84;} //droid
    if (type==45) {header=6811780; datasize=100;}//hook
    if (type==46) {header=6811928; datasize=88;} //defgen
    if ((type>46) and (type<62)) {header=6812080; datasize=108;} //weapon

    //mm
    if (type==64) {header=6813144; datasize=84;}




    if (header>0) {

    long newitem=CreateGameObject(datasize);
    if (newitem>4) {
        val=newitem;
        i=ReadLong(DataAddr()+32); //GalaxyItemId
        WriteLong(DataAddr()+32,i+1);
        WriteLong(newitem,header);
        WriteLong(newitem+8,i);
        WriteLong(newitem+12,type);
        WriteLong(newitem+24,size);
        if (race<5) {WriteByte(newitem+28,race);}
        if (race==5) {WriteByte(newitem+28,6);} //race none
        if (race>5) {WriteByte(newitem+28,5);WriteByte(newitem+74,race-6);}//6-blazer,7-keller,8-terron
        WriteDouble(newitem+56,100);

        if ((type>39) and (type<62)) {WriteByte(newitem+80,level);}
        if (type==39) {WriteByte(newitem+84,level);}
        if (type==22) {WriteLong(newitem+80,level);} // beacon charge
        if (type==64) {WriteByte(newitem+72,level);WriteByte(newitem+80,level-1);WriteLong(newitem+32,100);}
        if ((type>9) and (type<39)) {WriteByte(newitem+32,100);}


        if (type==39) {WriteByte(newitem+85,level*2-1);WriteByte(newitem+86,0);WriteByte(newitem+87,80);}

        if (type==40) {WriteLong(newitem+84,5*(level+1)+(size+1-(level%2))/2);WriteLong(newitem+88,5*(level+1)+(size+1-(level%2))/2);}

        if (type==41) {i=level; if (i>3) {i=2*i-3;} WriteLong(newitem+84,350+50*i); WriteByte(newitem+88,15+2*i);}

        if (type==42){switch (level){
        case 1: WriteLong(newitem+84,1200); break;
        case 2: WriteLong(newitem+84,1500); break;
        case 3: WriteLong(newitem+84,1800); break;
        case 4: WriteLong(newitem+84,2400); break;
        case 5: WriteLong(newitem+84,2700); break;
        case 6: WriteLong(newitem+84,3100); break;
        case 7: WriteLong(newitem+84,3500); break;
        case 8: WriteLong(newitem+84,4000); break;
        }}

        if (type==43) {WriteByte(newitem+81,level*5+1);}

        if (type==44) {i=level; if (i>4) {i=2*i-4;} WriteByte(newitem+81,5*i);}

        if (type==42){WriteLong(newitem+88,90+level*10);
            switch (level){
        case 1: WriteFloat(newitem+92,1);WriteFloat(newitem+96,3);WriteLong(newitem+84,40); break;
        case 2: WriteFloat(newitem+92,1);WriteFloat(newitem+96,4);WriteLong(newitem+84,50); break;
        case 3: WriteFloat(newitem+92,2);WriteFloat(newitem+96,4);WriteLong(newitem+84,60); break;
        case 4: WriteFloat(newitem+92,3);WriteFloat(newitem+96,5);WriteLong(newitem+84,80); break;
        case 5: WriteFloat(newitem+92,3);WriteFloat(newitem+96,6);WriteLong(newitem+84,90); break;
        case 6: WriteFloat(newitem+92,4);WriteFloat(newitem+96,6);WriteLong(newitem+84,100); break;
        case 7: WriteFloat(newitem+92,5);WriteFloat(newitem+96,7);WriteLong(newitem+84,150);WriteLong(newitem+88,175); break;
        case 8: WriteFloat(newitem+92,7);WriteFloat(newitem+96,8);WriteLong(newitem+84,500);WriteLong(newitem+88,200); break;
        }}

        if (type==44) {EqDefGenProperty(newitem,level*5);}


        if ((type>46) and (type<62)) {
            if (type==47){
                switch (level){
                case 1: WriteByte(newitem+88,10); WriteByte(newitem+89,15); WriteLong(newitem+84,270); break;
                case 2: WriteByte(newitem+88,11); WriteByte(newitem+89,16); WriteLong(newitem+84,285); break;
                case 3: WriteByte(newitem+88,12); WriteByte(newitem+89,17); WriteLong(newitem+84,285); break;
                case 4: WriteByte(newitem+88,12); WriteByte(newitem+89,18); WriteLong(newitem+84,300); break;
                case 5: WriteByte(newitem+88,14); WriteByte(newitem+89,21); WriteLong(newitem+84,300); break;
                case 6: WriteByte(newitem+88,16); WriteByte(newitem+89,24); WriteLong(newitem+84,315); break;
                case 7: WriteByte(newitem+88,19); WriteByte(newitem+89,28); WriteLong(newitem+84,315); break;
                case 8: WriteByte(newitem+88,23); WriteByte(newitem+89,34); WriteLong(newitem+84,330); break;
                case 10: WriteByte(newitem+88,25); WriteByte(newitem+89,38); WriteLong(newitem+84,330); break;
                }}
            if (type==48){
                switch (level){
                case 1: WriteByte(newitem+88,15); WriteByte(newitem+89,25); WriteLong(newitem+84,216); break;
                case 2: WriteByte(newitem+88,18); WriteByte(newitem+89,30); WriteLong(newitem+84,228); break;
                case 3: WriteByte(newitem+88,21); WriteByte(newitem+89,35); WriteLong(newitem+84,228); break;
                case 4: WriteByte(newitem+88,24); WriteByte(newitem+89,40); WriteLong(newitem+84,240); break;
                case 5: WriteByte(newitem+88,27); WriteByte(newitem+89,45); WriteLong(newitem+84,240); break;
                case 6: WriteByte(newitem+88,30); WriteByte(newitem+89,50); WriteLong(newitem+84,252); break;
                case 7: WriteByte(newitem+88,33); WriteByte(newitem+89,55); WriteLong(newitem+84,252); break;
                case 8: WriteByte(newitem+88,36); WriteByte(newitem+89,60); WriteLong(newitem+84,264); break;
                case 10: WriteByte(newitem+88,52); WriteByte(newitem+89,88); WriteLong(newitem+84,264); break;
                }}
            if (type==49){
                switch (level){
                case 1: WriteByte(newitem+88,8); WriteByte(newitem+89,24); WriteLong(newitem+84,315); break;
                case 2: WriteByte(newitem+88,9); WriteByte(newitem+89,26); WriteLong(newitem+84,322); break;
                case 3: WriteByte(newitem+88,9); WriteByte(newitem+89,28); WriteLong(newitem+84,322); break;
                case 4: WriteByte(newitem+88,10); WriteByte(newitem+89,29); WriteLong(newitem+84,350); break;
                case 5: WriteByte(newitem+88,10); WriteByte(newitem+89,30); WriteLong(newitem+84,350); break;
                case 6: WriteByte(newitem+88,10); WriteByte(newitem+89,31); WriteLong(newitem+84,367); break;
                case 7: WriteByte(newitem+88,12); WriteByte(newitem+89,36); WriteLong(newitem+84,367); break;
                case 8: WriteByte(newitem+88,16); WriteByte(newitem+89,48); WriteLong(newitem+84,385); break;
                case 10: WriteByte(newitem+88,32); WriteByte(newitem+89,96); WriteLong(newitem+84,385); break;
                }}
            if (type==50){
                switch (level){
                case 1: WriteByte(newitem+88,10); WriteByte(newitem+89,12); WriteLong(newitem+84,450); break;
                case 2: WriteByte(newitem+88,12); WriteByte(newitem+89,14); WriteLong(newitem+84,475); break;
                case 3: WriteByte(newitem+88,14); WriteByte(newitem+89,17); WriteLong(newitem+84,475); break;
                case 4: WriteByte(newitem+88,16); WriteByte(newitem+89,19); WriteLong(newitem+84,500); break;
                case 5: WriteByte(newitem+88,18); WriteByte(newitem+89,22); WriteLong(newitem+84,500); break;
                case 6: WriteByte(newitem+88,21); WriteByte(newitem+89,25); WriteLong(newitem+84,525); break;
                case 7: WriteByte(newitem+88,25); WriteByte(newitem+89,30); WriteLong(newitem+84,525); break;
                case 8: WriteByte(newitem+88,30); WriteByte(newitem+89,36); WriteLong(newitem+84,550); break;
                case 10: WriteByte(newitem+88,30); WriteByte(newitem+89,36); WriteLong(newitem+84,550); break;
                }}
            if (type==51){
                switch (level){
                case 1: WriteByte(newitem+88,5); WriteByte(newitem+89,10); WriteLong(newitem+84,342); break;
                case 2: WriteByte(newitem+88,6); WriteByte(newitem+89,11); WriteLong(newitem+84,361); break;
                case 3: WriteByte(newitem+88,6); WriteByte(newitem+89,11); WriteLong(newitem+84,361); break;
                case 4: WriteByte(newitem+88,6); WriteByte(newitem+89,12); WriteLong(newitem+84,380); break;
                case 5: WriteByte(newitem+88,6); WriteByte(newitem+89,12); WriteLong(newitem+84,380); break;
                case 6: WriteByte(newitem+88,6); WriteByte(newitem+89,13); WriteLong(newitem+84,399); break;
                case 7: WriteByte(newitem+88,7); WriteByte(newitem+89,14); WriteLong(newitem+84,399); break;
                case 8: WriteByte(newitem+88,8); WriteByte(newitem+89,15); WriteLong(newitem+84,418); break;
                case 10: WriteByte(newitem+88,28); WriteByte(newitem+89,55); WriteLong(newitem+84,418); break;
                }}
            if (type==52){
                switch (level){
                case 1: WriteByte(newitem+88,20); WriteByte(newitem+89,30); WriteLong(newitem+84,216); break;
                case 2: WriteByte(newitem+88,22); WriteByte(newitem+89,33); WriteLong(newitem+84,228); break;
                case 3: WriteByte(newitem+88,23); WriteByte(newitem+89,34); WriteLong(newitem+84,228); break;
                case 4: WriteByte(newitem+88,25); WriteByte(newitem+89,36); WriteLong(newitem+84,240); break;
                case 5: WriteByte(newitem+88,25); WriteByte(newitem+89,38); WriteLong(newitem+84,240); break;
                case 6: WriteByte(newitem+88,26); WriteByte(newitem+89,39); WriteLong(newitem+84,252); break;
                case 7: WriteByte(newitem+88,30); WriteByte(newitem+89,45); WriteLong(newitem+84,252); break;
                case 8: WriteByte(newitem+88,36); WriteByte(newitem+89,54); WriteLong(newitem+84,264); break;
                }}
            if (type==53){
                switch (level){
                case 1: WriteByte(newitem+88,10); WriteByte(newitem+89,40); WriteLong(newitem+84,306); break;
                case 2: WriteByte(newitem+88,11); WriteByte(newitem+89,44); WriteLong(newitem+84,323); break;
                case 3: WriteByte(newitem+88,11); WriteByte(newitem+89,46); WriteLong(newitem+84,323); break;
                case 4: WriteByte(newitem+88,12); WriteByte(newitem+89,48); WriteLong(newitem+84,340); break;
                case 5: WriteByte(newitem+88,12); WriteByte(newitem+89,50); WriteLong(newitem+84,340); break;
                case 6: WriteByte(newitem+88,13); WriteByte(newitem+89,52); WriteLong(newitem+84,357); break;
                case 7: WriteByte(newitem+88,15); WriteByte(newitem+89,60); WriteLong(newitem+84,357); break;
                case 8: WriteByte(newitem+88,17); WriteByte(newitem+89,68); WriteLong(newitem+84,374); break;
                case 10: WriteByte(newitem+88,60); WriteByte(newitem+89,240); WriteLong(newitem+84,374); break;
                }}
            if (type==54){
                switch (level){
                case 1: WriteByte(newitem+88,5); WriteByte(newitem+89,35); WriteLong(newitem+84,297); break;
                case 2: WriteByte(newitem+88,6); WriteByte(newitem+89,38); WriteLong(newitem+84,314); break;
                case 3: WriteByte(newitem+88,6); WriteByte(newitem+89,42); WriteLong(newitem+84,314); break;
                case 4: WriteByte(newitem+88,6); WriteByte(newitem+89,46); WriteLong(newitem+84,330); break;
                case 5: WriteByte(newitem+88,7); WriteByte(newitem+89,49); WriteLong(newitem+84,330); break;
                case 6: WriteByte(newitem+88,8); WriteByte(newitem+89,52); WriteLong(newitem+84,346); break;
                case 7: WriteByte(newitem+88,8); WriteByte(newitem+89,56); WriteLong(newitem+84,346); break;
                case 8: WriteByte(newitem+88,8); WriteByte(newitem+89,60); WriteLong(newitem+84,363); break;
                }}
            if (type==55){
                switch (level){
                case 1: WriteByte(newitem+88,20); WriteByte(newitem+89,45); WriteLong(newitem+84,270); break;
                case 2: WriteByte(newitem+88,22); WriteByte(newitem+89,49); WriteLong(newitem+84,285); break;
                case 3: WriteByte(newitem+88,23); WriteByte(newitem+89,52); WriteLong(newitem+84,285); break;
                case 4: WriteByte(newitem+88,24); WriteByte(newitem+89,54); WriteLong(newitem+84,300); break;
                case 5: WriteByte(newitem+88,25); WriteByte(newitem+89,56); WriteLong(newitem+84,300); break;
                case 6: WriteByte(newitem+88,26); WriteByte(newitem+89,58); WriteLong(newitem+84,315); break;
                case 7: WriteByte(newitem+88,27); WriteByte(newitem+89,61); WriteLong(newitem+84,315); break;
                case 8: WriteByte(newitem+88,28); WriteByte(newitem+89,63); WriteLong(newitem+84,330); break;
                }}
            if (type==56){
                switch (level){
                case 1: WriteByte(newitem+88,30); WriteByte(newitem+89,45); WriteLong(newitem+84,288); break;
                case 2: WriteByte(newitem+88,33); WriteByte(newitem+89,49); WriteLong(newitem+84,304); break;
                case 3: WriteByte(newitem+88,34); WriteByte(newitem+89,52); WriteLong(newitem+84,304); break;
                case 4: WriteByte(newitem+88,36); WriteByte(newitem+89,54); WriteLong(newitem+84,320); break;
                case 5: WriteByte(newitem+88,38); WriteByte(newitem+89,56); WriteLong(newitem+84,320); break;
                case 6: WriteByte(newitem+88,39); WriteByte(newitem+89,58); WriteLong(newitem+84,336); break;
                case 7: WriteByte(newitem+88,40); WriteByte(newitem+89,61); WriteLong(newitem+84,336); break;
                case 8: WriteByte(newitem+88,42); WriteByte(newitem+89,63); WriteLong(newitem+84,352); break;
                }}
            if (type==57){
                switch (level){
                case 1: WriteByte(newitem+88,25); WriteByte(newitem+89,50); WriteLong(newitem+84,342); break;
                case 2: WriteByte(newitem+88,27); WriteByte(newitem+89,55); WriteLong(newitem+84,361); break;
                case 3: WriteByte(newitem+88,29); WriteByte(newitem+89,58); WriteLong(newitem+84,361); break;
                case 4: WriteByte(newitem+88,30); WriteByte(newitem+89,60); WriteLong(newitem+84,380); break;
                case 5: WriteByte(newitem+88,31); WriteByte(newitem+89,62); WriteLong(newitem+84,380); break;
                case 6: WriteByte(newitem+88,32); WriteByte(newitem+89,65); WriteLong(newitem+84,399); break;
                case 7: WriteByte(newitem+88,34); WriteByte(newitem+89,68); WriteLong(newitem+84,399); break;
                case 8: WriteByte(newitem+88,35); WriteByte(newitem+89,70); WriteLong(newitem+84,418); break;
                }}
            if (type==58){
                switch (level){
                case 1: WriteByte(newitem+88,40); WriteByte(newitem+89,60); WriteLong(newitem+84,288); break;
                case 2: WriteByte(newitem+88,42); WriteByte(newitem+89,66); WriteLong(newitem+84,304); break;
                case 3: WriteByte(newitem+88,44); WriteByte(newitem+89,69); WriteLong(newitem+84,304); break;
                case 4: WriteByte(newitem+88,46); WriteByte(newitem+89,72); WriteLong(newitem+84,320); break;
                case 5: WriteByte(newitem+88,48); WriteByte(newitem+89,75); WriteLong(newitem+84,320); break;
                case 6: WriteByte(newitem+88,50); WriteByte(newitem+89,78); WriteLong(newitem+84,336); break;
                case 7: WriteByte(newitem+88,52); WriteByte(newitem+89,81); WriteLong(newitem+84,336); break;
                case 8: WriteByte(newitem+88,54); WriteByte(newitem+89,84); WriteLong(newitem+84,352); break;
                }}
            if (type==59){
                switch (level){
                case 1: WriteByte(newitem+88,20); WriteByte(newitem+89,30); WriteLong(newitem+84,270); break;
                case 2: WriteByte(newitem+88,22); WriteByte(newitem+89,33); WriteLong(newitem+84,285); break;
                case 3: WriteByte(newitem+88,25); WriteByte(newitem+89,47); WriteLong(newitem+84,285); break;
                case 4: WriteByte(newitem+88,28); WriteByte(newitem+89,42); WriteLong(newitem+84,300); break;
                case 5: WriteByte(newitem+88,36); WriteByte(newitem+89,54); WriteLong(newitem+84,300); break;
                case 6: WriteByte(newitem+88,44); WriteByte(newitem+89,66); WriteLong(newitem+84,315); break;
                case 7: WriteByte(newitem+88,52); WriteByte(newitem+89,78); WriteLong(newitem+84,315); break;
                case 8: WriteByte(newitem+88,60); WriteByte(newitem+89,90); WriteLong(newitem+84,330); break;
                case 10: WriteByte(newitem+88,120); WriteByte(newitem+89,180); WriteLong(newitem+84,330); break;
                }}
            if (type==60){
                switch (level){
                case 1: WriteByte(newitem+88,18); WriteByte(newitem+89,40); WriteLong(newitem+84,297); break;
                case 2: WriteByte(newitem+88,20); WriteByte(newitem+89,44); WriteLong(newitem+84,314); break;
                case 3: WriteByte(newitem+88,22); WriteByte(newitem+89,50); WriteLong(newitem+84,314); break;
                case 4: WriteByte(newitem+88,25); WriteByte(newitem+89,56); WriteLong(newitem+84,330); break;
                case 5: WriteByte(newitem+88,32); WriteByte(newitem+89,72); WriteLong(newitem+84,330); break;
                case 6: WriteByte(newitem+88,40); WriteByte(newitem+89,88); WriteLong(newitem+84,346); break;
                case 7: WriteByte(newitem+88,47); WriteByte(newitem+89,104); WriteLong(newitem+84,346); break;
                case 8: WriteByte(newitem+88,54); WriteByte(newitem+89,120); WriteLong(newitem+84,363); break;
                }}
            if (type==61){
                switch (level){
                case 1: WriteByte(newitem+88,25); WriteByte(newitem+89,30); WriteLong(newitem+84,720); break;
                case 2: WriteByte(newitem+88,27); WriteByte(newitem+89,33); WriteLong(newitem+84,760); break;
                case 3: WriteByte(newitem+88,31); WriteByte(newitem+89,37); WriteLong(newitem+84,760); break;
                case 4: WriteByte(newitem+88,35); WriteByte(newitem+89,42); WriteLong(newitem+84,800); break;
                case 5: WriteByte(newitem+88,45); WriteByte(newitem+89,54); WriteLong(newitem+84,800); break;
                case 6: WriteByte(newitem+88,55); WriteByte(newitem+89,66); WriteLong(newitem+84,840); break;
                case 7: WriteByte(newitem+88,65); WriteByte(newitem+89,78); WriteLong(newitem+84,840); break;
                case 8: WriteByte(newitem+88,75); WriteByte(newitem+89,90); WriteLong(newitem+84,880); break;
                }}

        WriteLong(newitem+100,25+level*5);
        WriteLong(newitem+104,25+level*5);
        if (level==10) {WriteLong(newitem+100,150);
                        WriteLong(newitem+104,150);}
         }

        if ((type>38) and (type<62)) {WriteLong(newitem+32,1000*level*level);}
    }}
return val;}




long __stdcall GetItemFromShip(const long ship, const long num) //GetItemFromShip@8 //116
  {long val=0; long itemtype=0;
   long i=ReadLong(ship+732);
   long count=ReadLong(i+8);
   if ((num<count+1) and (num>0)) {val=RemoveObjectFromList(i,num);
            itemtype=ReadLong(val+12); // проверить игрока с его переключениями эквипов
            if ((itemtype<62) and (ReadLong(val+52)==1)) { //item used
            WriteLong(val+52,0);
            if ((itemtype>38) and (itemtype<47)) {WriteLong(ship+240+(itemtype-39)*4,0);} // желательно, конечно, не отнимать у корабля корпус,двигатель и бак :)
            if (itemtype>46) {WriteLong(ship+268+ReadByte(val+68)*4,0);}
            WriteByte(val+68,0);
        }}
 return val;}

long __stdcall GetArtFromShip(const long ship, const long num) //GetArtFromShip@8 //117
  {long val=0;
   long i=ReadLong(ship+736);
   long count=ReadLong(i+8);
   if ((num<count+1) and (num>0)) {val=RemoveObjectFromList(i,num);WriteLong(val+52,0);WriteByte(val+68,0);}
 return val;}


long __stdcall PutItemInShip(const long ship, const long item) //PutItemInShip@8 //118
{   long i=0;
    if ((GeneralItemProperty(item,1,0)<39) and (GeneralItemProperty(item,1,0)>8)) {i=ReadLong(ship+736);}
                else {i=ReadLong(ship+732);}
    return AddObjectToList(i,item);}


long __stdcall GetItemFromShop(const long obj, const long num) //GetItemFromShop@8 //119
{   long val=0; long ofs=0;
    long objheader=ReadLong(obj);
    if ((objheader==6465444) or (objheader==5276056) or (objheader==5282716) or (objheader==5289956)
        or (objheader==5297104) or (objheader==5304092) or (objheader==5310656)) {
    ofs=956;
    if (objheader==6465444) {ofs=292;}}
    long i=ReadLong(obj+ofs);
    long count=ReadLong(i+8);
    if ((num<count+1) and (num>0)) {val=RemoveObjectFromList(i,num);}
    return val;}

long __stdcall PutItemInShop(const long obj, const long item) //PutItemInShop@8 //120
{   long val=0; long ofs=0; long i=0;
    long objheader=ReadLong(obj);
    if ((objheader==6465444) or (objheader==5276056) or (objheader==5282716) or (objheader==5289956)
        or (objheader==5297104) or (objheader==5304092) or (objheader==5310656)) {
        ofs=956;
    if (objheader==6465444) {ofs=292;}}
    if (ofs>0) {i=ReadLong(obj+ofs); if (i==0) {i=CreateEmptyList(7315708);}
        val=AddObjectToList(i,item);}
    return val;}


long __stdcall DigItemFromPlanet(const long planet, const long num) //GetItemFromShop@8 //121
{   long val=0; long i=ReadLong(planet+348);
    if (i>0) {long count=ReadLong(i+8);
        if ((num<count+1) and (num>0)) {val=ReadLong(12+ReadLong(ReadLong(i + 4) + 4*(num-1)));
            FreeGameObject(RemoveObjectFromList(i,num));}}
    return val;}



long __stdcall HideItemOnPlanet(const long planet, const long item, const long coord, const long depth) //HideItemOnPlanet@8 //122
{ long val=0;
    long i=ReadLong(planet+348);
    if (i==0) {i=CreateEmptyList(4271268);}
    long water=ReadLong(planet+320);
    long land=ReadLong(planet+328);
    long hill=ReadLong(planet+336);


    long landtype=0; long landmax=water;
    if (landmax<land) {landtype=1; landmax=land;}
    if (landmax<hill) {landtype=2; landmax=hill;}


    long coordx=coord/8;
    long coordy=coord%8;
    //long coordx=qrand()%8;
    //long coordy=qrand()%14;


    long itemhole=CreateGameObject(16);
    WriteLong(itemhole,coordx+coordy*256+landtype*256*256);
    WriteLong(itemhole+4,landmax*depth/100); //depth=0..100
    WriteLong(itemhole+8,0);
    WriteLong(itemhole+12,item);
    AddObjectToList(i,itemhole);

    WriteLong(planet+324,0);
    WriteLong(planet+332,0);
    WriteLong(planet+340,0);

return val;}

//------------------------------------location-------------------------------------------------------


long __stdcall Distance(const long ship, const long obj) //Distance@8 //130
{long val=0; long i=0; long j=0;
 long shipx=CoordX(ship,0); long shipy=CoordY(ship,0); long shipstar=ShipToStar(ship);
 long header=shipstar; long objinstar=1; if (obj>0) {header=ReadLong(obj);objinstar=0;} //obj=0 -> distance to star
 long objx=CoordX(obj,0);long objy=CoordY(obj,0);
 long objx2=0;long objy2=0; long objinstar2=0; // for hole exit
 if (ShipToStar(obj)==shipstar) {objinstar=1;} //ship,missile

 if (header==6465444) {if (PlanetToStar(obj)==shipstar) {objinstar=1;}} //planet
 if (header==6308228) {if (ReadLong(obj+8)==shipstar) {objinstar=1;}} //asteroid
 if ((header>6811048-1) and (header<6817880+1)){ //item
    j=StarItems(shipstar,0);  while (i<j) {i=i+1; if (StarItems(shipstar,i)==obj) {objinstar=1;}}}
 if (header==6667296){ //hole
 objx2=CoordX(obj,1);objy2=CoordY(obj,1);
 if (ReadLong(obj+8)==shipstar) {objinstar=1;}
 if (ReadLong(obj+20)==shipstar) {objinstar2=1;} }

float dist=0; float dist2=0;
if (objinstar==1) {dist=sqrtR((shipx-objx)*(shipx-objx)+(shipy-objy)*(shipy-objy));}
if (objinstar2==1) {dist2=sqrtR((shipx-objx2)*(shipx-objx2)+(shipy-objy2)*(shipy-objy2));
    if (dist2<dist) {dist=dist2;}}
if (dist>127*256*256*256) {dist=127*256*256*256;}
 if (dist<-127*256*256*256) {dist=-127*256*256*256;}
val=dist;
return val;}

long __stdcall CoordX(const long obj, const long flag) //CoordX@8 //131
{   long val=ReadFloat(obj+16); //ships, missiles, items in space
    long header=ReadLong(obj);
    switch (header){
        case 6308228: val=ReadFloat(obj+12); break; //asteroid //float20
        case 6667428: val=ReadFloat(obj+24); break; //star
        case 6667296: //hole
            if (flag==0) {val=ReadFloat(obj+12);} else {val=ReadFloat(obj+24);} break; //0-in star, 1-to star
        case 6465444: val=(ReadDouble(obj+40)*sinG(ReadDouble(obj+32)));break; //planet
    }
    return val;}

long __stdcall CoordY(const long obj, const long flag) //CoordY@8 //132
{   long val=ReadFloat(obj+20); //ships, missiles, items in space
    long header=ReadLong(obj);
    switch (header){
        case 6308228: val=ReadFloat(obj+16); break; //asteroid //float24
        case 6667428: val=ReadFloat(obj+28); break; //star
        case 6667296: //hole
            if (flag==0) {val=ReadFloat(obj+16);} else {val=ReadFloat(obj+28);} break; //0-in star, 1-to star
        case 6465444: val=-(ReadDouble(obj+40)*cosG(ReadDouble(obj+32))); break; //planet
        }
    return val;}

double __stdcall cosG(const double phi) //cosG@8 //no number, not in FunManager list
{double psi=phi;
    while (psi>180) {psi=psi-360;} psi=psi/180*3.141592654;
    double psi2=psi*psi;
    double val=((((((psi2/182+1)*psi2/132-1)*psi2/90+1)*psi2/56-1)*psi2/30+1)*psi2/12-1)*psi2/2+1;
    return val;}

double __stdcall sinG(const double phi) //sinG@8 //no number, not in FunManager list
{double psi=phi;
    while (psi>180) {psi=psi-360;} psi=psi/180*3.141592654;
    double psi2=psi*psi;
    double val=psi*(((((((psi2/210+1)*psi2/156-1)*psi2/110+1)*psi2/72-1)*psi2/42+1)*psi2/20-1)*psi2/6+1);
    return val;}

double __stdcall sqrtR(const double x) //sqrtR@8 //no number, not in FunManager list
{   double x0=x;
    if (x0>127*256*256*256) {x0=127*256*256*256;}
    if (x0<-127*256*256*256) {x0=-127*256*256*256;}
    double y0=0; double y1=(x0+1)/2;
    while (((y1-y0)>0.1) or ((y0-y1)>0.1))  {y0=y1;y1=(y1+x0/y1)/2;}
    return y1;} // может притормаживать на очень больших числах




//------------------------------------player-------------------------------------------------------

long __stdcall Player() //Player@0 //no number
{   long count=GalaxyRangers(0);
    long val=GalaxyRangers(1);
    long i=1;
    while ((!(ReadLong(val)==5753428)) and (i<count)){i=i+1;val=GalaxyRangers(i);}
    return val;}


long __stdcall PlayerPrograms(const long property, const long value) //PlayerPrograms@8 //140
{   long val=0; long ship=Player();
    if (ReadLong(ship)==5753428) {
    if ((property>0) and (property<12)){
                     val=ReadLong(ship + 1012+property*4);
                     if (value>-1) {WriteLong(ship + 1012+property*4,value);};
                 }} //property = 1..11 = logical negation,dematerial,energotron,sub modem,intercom,shipwreck,weapon block,insanity,shock,self-destruction,disconnect
    return val;}


//deposit, etc


//------------------------------------ships-------------------------------------------------------


long __stdcall GalaxyShips(const long shipid, const long flag) //GalaxyShips@8 //150
{long val=0; int i=1;int j=0; int k=0; long star=0; //flag==0 - just number (cycle counter), flag<>0 - ID
long starscount=GalaxyStars(0);long shipcount=0; int flag2=0;
while (i<starscount+1) {
    j=1;
    star=ReadLong(ReadLong(ReadLong(DataAddr()+44)+4)+(i-1)*4);
    while ((j<StarShips(star,0)+1) and (flag2==0)){
        k=StarShips(star,j); shipcount=shipcount+1;
        if ((ReadLong(k+4)==shipid) and not(flag==0)) {val=k;flag2=1;}
        if ((shipcount==shipid) and (flag==0)) {val=k;flag2=1;}
        j=j+1;
       }
    i=i+1;}
if (shipid==0) {val=shipcount;}
return val;}

long __stdcall GalaxyRangers(const long num) //GalaxyRangers@4 //151
{   long val=0;
    long i=ReadLong(DataAddr()+56);
    long count=ReadLong(i+8);
    val=count;
    if ((num>0) and (num<count+1)) {val=ReadLong(ReadLong(i + 4) + 4*(num-1));}
    return val;}


long __stdcall StarShips(const long Star, const long num) //StarShips@8 //152
{   long val=0; long pl=0; long pn=0; long ms=0; long mn=0; long tmpshp=0; long tmppln=0;
    long i=ReadLong(Star+48);
    if (i>0) {long count=ReadLong(i+8);
    if ((num>0) and (num<count+1)) {val=ReadLong(ReadLong(i + 4) + 4*(num-1));}
    if ((num>count) or (num<1)) {
        pn=StarPlanets(Star,0);
        while (pl<pn){
          pl=pl+1;
          tmppln=StarPlanets(Star,pl);
          mn=PlanetMilitary(tmppln,0);
          ms=0;
          while (ms<mn){ms=ms+1; tmpshp=PlanetMilitary(tmppln,ms); if ((ReadLong(24+tmpshp)==tmppln) and (ReadLong(840+tmpshp)==0)){ // этот корабль спит на планете
              count=count+1;
              if (num==count){val=tmpshp;ms=mn;pl=pn;}}
          }}}
    if (val==0) {val=count;}}
    return val;} //нумерация здесь - в порядке прилета в систему, после всех - сидящие на своей планете воен. корабли


long __stdcall PlanetMilitary(const long planet, const long num) //PlanetMilitary@8 //153
{   long val=0;
    long i=ReadLong(planet+296);
    if (i>0) {long count=ReadLong(i+8);
    if ((num>0) and (num<count+1)) {val=ReadLong(ReadLong(i + 4) + 4*(num-1));}
    if (num==0) {val=count;}}
    return val;}


long __stdcall ShipStats(const long ship, const long property, const long value) //ShipStats@12 //154
{   long val=0;
    byte type=ReadByte(ship+12);
    switch (property){
                     case 1: //race
                     val=ReadByte(ship + 13);
                     if ((value>-1) and (value<5)) {WriteByte(ship + 13,value);}; //установка доминаторской расы обычным кораблям приведет к крашу
                     break;                                                       //изменение расы игрока тоже может привести к крашу (не сразу а при открытии окна корабля - видно портрет не грузится)
                     case 2: //type
                     val=type;
                     if ((value>-1) and (value<12)) {WriteByte(ship + 12,value);}; //изменение типа корабля нежелательно
                     break;
                     case 3: //rank
                     if (type>0) {val=ReadByte(ship + 976);
                        if ((value>-1) and (value<7)) {WriteByte(ship + 976,value);};};
                     break;
                     case 4: //new rank
                     if (type>0) {val=ReadLong(ship + 976+2); // тут возможны проблемы, если этот параметр на самом деле имеет тип word. Если dword, то нет проблем
                        if (value>-1) {WriteLong(ship + 976+2,value);};};
                     break;
                     case 5: //exp
                     if (type>0) {val=ReadLong(ship + 716);
                        if (value>-1) {WriteLong(ship + 716,value);};};
                     break;
                     case 6: //new exp
                     if (type>0) {val=ReadLong(ship + 716+4);
                        if (value>-1) {WriteLong(ship + 716+4,value);};};
                     break;
                     case 7: //nodes count
                     if (type>0) {val=ReadLong(ship + 1012);
                        if (value>-1) {WriteLong(ship + 1012,value);};};
                     break;
                     case 8: //rating trader
                     if (type==1) {val=ReadByte(ship + 986);
                        if ((value>-1) and (value<101)) {WriteByte(ship + 986,value);};};
                     break;
                     case 9: //rating pirate
                     if (type==1) {val=ReadByte(ship + 987);
                        if ((value>-1) and (value<101)) {WriteByte(ship + 987,value);};};
                     break;
                     case 10: //rating warrior
                     if (type==1) {val=ReadByte(ship + 988);
                        if ((value>-1) and (value<101)) {WriteByte(ship + 988,value);};};
                     break;
                     case 11: //current planet // если сейчас не в планете - 0? не проверял
                     val=ReadLong(ship + 24);
                     //if (value>0) {WriteLong(ship + 24,value);};
                     break;
                     case 12: //current ruins
                     val=ReadLong(ship + 28);
                     //if (value>0) {WriteLong(ship + 28,value);};
                     break;
                     case 13: //current star
                     val=ReadLong(ship + 32);
                     //if (value>0) {WriteLong(ship + 32,value);};
                     break;
                     case 14: //home star
                     val=ReadLong(ship + 36);
                     if (value>0) {WriteLong(ship + 36,value);};
                     break;
                     case 15: //home planet
                     val=ReadLong(ship + 40);
                     if (value>0) {WriteLong(ship + 40,value);};
                     break;


                 }
    return val;}

long __stdcall ShipSkillsData(const long ship, const long property, const long value, const long flag) //ShipSkillsData@16 //155
{   int val=0; //flag = 0 - natural skills, flag <>0(1) - modified skills, flag = 1 - normalized skills
   if ((property>0) and (property<7)){
                   val=ReadByte(ship + 293+property);
                   if ((value>-1) and (value<6) and (flag==0)) {WriteByte(ship + 293+property,value);}
                   if (not(flag==0)){
                     long acc=ReadByte(ship + 294);
                     long mob=ReadByte(ship + 295);
                     long tech=ReadByte(ship + 296);
                     long trade=ReadByte(ship + 297);
                     long charm=ReadByte(ship + 298);
                     long lead=ReadByte(ship + 299);
                     if (HealthFactor(ship,1,0)>0) {acc=acc-3; mob=mob-3; tech=tech-3; trade=trade-3;} //blindness
                     if (HealthFactor(ship,3,0)>0) {acc=acc+1; mob=mob+1; charm=charm-1; lead=lead+2;} //fanaticizm
                     if (HealthFactor(ship,5,0)>0) {acc=acc-2; charm=charm+3;} //luatan
                     if (HealthFactor(ship,6,0)>0) {acc=acc-3; mob=mob-3; tech=tech-2;} //narco
                     if (HealthFactor(ship,7,0)>0) {acc=acc-2; mob=mob-5; trade=trade-10;} //contuz
                     if (HealthFactor(ship,8,0)>0) {acc=acc-2; mob=mob-2; tech=tech-2; charm=charm-1; lead=lead-1;} //rastyaj
                     if (HealthFactor(ship,9,0)>0) {trade=trade+3; lead=lead+3;} //malososus
                     if (HealthFactor(ship,10,0)>0) {tech=tech-10;} //pelenosha
                     if (HealthFactor(ship,11,0)>0) {acc=acc-1; tech=tech-2; trade=trade+2;} //aka seciyanka
                     if (HealthFactor(ship,12,0)>0) {acc=acc+1; mob=mob+1;} //new molizon
                     if (HealthFactor(ship,13,0)>0) {acc=acc+4; mob=mob+3;} //maloc sija
                     if (HealthFactor(ship,14,0)>0) {charm=charm-1; lead=lead-1;} //hamas
                     if (HealthFactor(ship,15,0)>0) {acc=acc+1; mob=mob+1; tech=tech+1; trade=trade+1;} //stardust
                     if (HealthFactor(ship,16,0)>0) {tech=tech+5;} //super tech
                     if (HealthFactor(ship,17,0)>0) {acc=acc+4; mob=mob+2;} //gaalistra
                     if (HealthFactor(ship,19,0)>0) {charm=charm+10;} //ragobam
                     if (HealthFactor(ship,20,0)>0) {charm=charm+1; lead=lead+4;} //shahmandu
                     if (HealthFactor(ship,21,0)>0) {charm=charm-3;} //psy-kesh
                     if (HealthFactor(ship,22,0)>0) {trade=trade+8;} //markirovka
                     if (HealthFactor(ship,23,0)>0) {acc=acc-1; mob=mob-1;} //dublplex
                     if (HealthFactor(ship,24,0)>0) {charm=charm+2;} //abs status
                     switch (property){
                      case 1: val=acc; break;
                      case 2: val=mob; break;
                      case 3: val=tech; break;
                      case 4: val=trade; break;
                      case 5: val=charm; break;
                      case 6: val=lead; break;
                     }
                     if (flag==1) {val=qMin(qMax(val,0),5);}
                 }
              } //property = 1..6 = accuracy,mobility,engineering,trade,charm,leaderShip
    return val;}

long __stdcall HealthFactor(const long ship, const long num, const long value) //CheckHealthFactor@12 //156
{   long val=1; long status = ReadLong(ship + 292+num*16);
   if ((num>0) and (num<26)){
       if ((status==0+0*256+89*256*256+64*256*256*256) or ((num==25) and (status>0))) {val=ReadLong(ship + 292+num*16+8);}
       else if (status==0) {val=0;}
       if ((val>1) and (value>0)) {WriteLong(ship + 292+num*16+8,value);}}
    return val;} //num =  1..12-illness, 13..24-stim 25-beam.ill  //возвращает (0) если нет у корабля такого стима/болезни, (дату), до которой действует, если есть, (1) если есть, но в скрытой форме

long __stdcall ClearHealthFactor(const long ship, const long num) //ClearHealthFactor@8 //157
{   if ((num>0) and (num<26)){
        WriteLong(ship + 292+num*16,0);
        WriteLong(ship + 292+num*16+4,0);
        WriteLong(ship + 292+num*16+8,0);}
    return 0;} //num =  1..12-illness, 13..24-stim 25-beam.ill

long __stdcall AddHealthFactor(const long ship, const long num, const long end, const long stat) //AddHealthFactor@16 //158
{   long status=stat; if (status==0) {status=0+0*256+89*256*256+64*256*256*256;}
    const long start=GalaxyData(1,0);
    if ((num>0) and (num<26)){
        // возможно, поставив ниже другие значения вместо 0 0 89 64 можно прицепить
        WriteLong(ship + 292+num*16,status); // болезнь в скрытой форме (когда эффекта еще нет, но биомир уже сигналит желтым, и на мед.базе ее видят)
        WriteLong(ship + 292+num*16+4,start); // или в неизлечимой форме, когда можно только ждать выздоровления (у лучевой болезни например здесь стоит 0 0 224 63)
        WriteLong(ship + 292+num*16+8,end);} // у непроявленной болезни было 254 255 88 64.  Но я это не проверял
    return 0;} //num =  1..12-illness, 13..24-stim 25-beam.ill

//ship medals

long __stdcall ShipMedals(const long ship, const long num) //ShipMedal@8 //159
{long medalcount=ReadLong(ship+768); long val=medalcount;
if ((num>0) and (num<medalcount+1)) {val=ReadByte(ReadLong(ReadLong(ship+764)+4)+(num-1)*4);}
return val;}

long __stdcall ShipMedalChange(const long ship, const long num, const long medal) //ShipMedalChange@12 //160
{long medalcount=ReadLong(ship+768); long val=0;
if ((num>0) and (num<medalcount+1)) {val=ReadByte(ReadLong(ReadLong(ship+764)+4)+(num-1)*4);
                                    WriteByte(ReadLong(ReadLong(ship+764)+4)+(num-1)*4,medal);} //0..47
return val;}

long __stdcall ShipAddMedal(const long ship, const long medal) //ShipAddMedal@8 //161
{long medalcount=ReadLong(ship+768); long val=medalcount+1;
 long medallist=ReadLong(ship+764);
 if (medalcount==0) {medallist=CreateEmptyList(4271268);
                        WriteLong(ship+764,medallist);}
 long newmedal=CreateGameObject(8);
 //if (medalcount==0) {WriteLong(newmedal,newmedal);WriteByte(newmedal+4,12);}
 WriteByte(newmedal,medal);
 //WriteByte(newmedal+4,12); //не знаю, для чего это там
 AddObjectToList(medallist,newmedal);
 WriteLong(ship+768,medalcount+1);
return val;}

long __stdcall ShipRemoveMedal(const long ship, const long num) //ShipRemoveMedal@8 //162
{long medalcount=ReadLong(ship+768); long val=medalcount;
if ((num>0) and (num<medalcount+1)) {FreeGameObject(RemoveObjectFromList(ReadLong(ship+764),num));val=val-1;}
return val;}

long __stdcall ShipCountDuplicateMedals(const long ship, const long medal) //ShipCountDublicateMedals@12 //163
{long medalcount=ReadLong(ship+768); long val=0; long i=0;
    while (i<medalcount) {i=i+1; if (ShipMedals(ship,i)==medal) {val=val+1;}}
return val;}



long __stdcall ShipSetSkin(const long ship, const long faction, const long type) //ShipSetSkin@12 //164
{long skin=ReadLong(ReadLong(ship+872)+24);
long skin2=ReadLong(ReadLong(ship+872)+124);
long skin3=ReadLong(ReadLong(ship+872)+128);
long newsize=5; long newsize2=8;
if (faction<5) { //coalition ships
        switch(faction) {
        case 0: newsize=newsize+6;newsize2=newsize2+6; break; //maloc
        case 1: newsize=newsize+7;newsize2=newsize2+7;break; //peleng
        case 2: newsize=newsize+7;newsize2=newsize2+7;break; //people
        case 3: newsize=newsize+4;newsize2=newsize2+4;break; //fei
        case 4: newsize=newsize+5;newsize2=newsize2+5;break; //gaal
        }
        switch(type) {
        case 0: newsize=newsize+6;break; //ranger
        case 1: newsize=newsize+6;break; //pirate
        case 2: newsize=newsize+7;break; //warrior
        case 3: newsize=newsize+9;break; //transport
        case 4: newsize=newsize+5;break; //liner
        case 5: newsize=newsize+8;break; //diplomat
        }}

if (faction==5) {newsize=11;newsize2=9;} //uni-hull
if (faction==6) {newsize=17;newsize2=20;} //tranclucator

//ПРЕДУПРЕЖДЕНИЕ: привешивание обычному кораблю того, что что ниже - рандомно крушит игру,
// годно пока только для лулзов
if ((faction>6) and (faction<10)) {newsize=14;newsize2=15;} //dominators
if (faction==10) {newsize=8;newsize2=10;}//ab ships
if (faction==11) {newsize=9;newsize2=11;}//unknown



FreeGameObject(skin);skin=CreateEmptyString(newsize);
FreeGameObject(skin2);skin2=CreateEmptyString(newsize2);
FreeGameObject(skin3);if (faction<12) {skin3=CreateEmptyString(newsize2+1);}
                        else {skin3=CreateEmptyString(newsize2);}
WriteLong(ReadLong(ship+872)+24,skin);
WriteLong(ReadLong(ship+872)+124,skin2);
WriteLong(ReadLong(ship+872)+128,skin3);


WriteByte(skin+0,83); WriteByte(skin+2,104); WriteByte(skin+4,105); WriteByte(skin+6,112); WriteByte(skin+8,46);//Ship.
WriteByte(skin2+0,66); WriteByte(skin2+2,109); WriteByte(skin2+4,46); //Bm.Ship.
WriteByte(skin2+6,83); WriteByte(skin2+8,104); WriteByte(skin2+10,105); WriteByte(skin2+12,112); WriteByte(skin2+14,46);
long i=skin+10;long j=skin2+16;

if (faction<5) { //coalition ships
        switch(faction) {
        case 0: WriteByte(i,77); WriteByte(i+2,97); WriteByte(i+4,108); WriteByte(i+6,111); WriteByte(i+8,99); WriteByte(i+10,46); i=i+12;
                WriteByte(j,77); WriteByte(j+2,97); WriteByte(j+4,108); WriteByte(j+6,111); WriteByte(j+8,99); j=j+10; break; //Maloc.
        case 1: WriteByte(i,80); WriteByte(i+2,101); WriteByte(i+4,108); WriteByte(i+6,101); WriteByte(i+8,110); WriteByte(i+10,103); WriteByte(i+12,46); i=i+14;
                WriteByte(j,80); WriteByte(j+2,101); WriteByte(j+4,108); WriteByte(j+6,101); WriteByte(j+8,110); WriteByte(j+10,103); j=j+12; break; //Peleng.
        case 2: WriteByte(i,80); WriteByte(i+2,101); WriteByte(i+4,111); WriteByte(i+6,112); WriteByte(i+8,108); WriteByte(i+10,101); WriteByte(i+12,46); i=i+14;
                WriteByte(j,80); WriteByte(j+2,101); WriteByte(j+4,111); WriteByte(j+6,112); WriteByte(j+8,108); WriteByte(j+10,101); j=j+12; break; //People.
        case 3: WriteByte(i,70); WriteByte(i+2,101); WriteByte(i+4,105); WriteByte(i+6,46); i=i+8;
                WriteByte(j,70); WriteByte(j+2,101); WriteByte(j+4,105); j=j+6; break; //Fei.
        case 4: WriteByte(i,71); WriteByte(i+2,97); WriteByte(i+4,97); WriteByte(i+6,108); WriteByte(i+8,46); i=i+10;
                WriteByte(j,71); WriteByte(j+2,97); WriteByte(j+4,97); WriteByte(j+6,108); j=j+8; break; //Gaal.
        }
        switch(type) {
        case 0: WriteByte(j,82); WriteByte(i,82); WriteByte(i+2,97); WriteByte(i+4,110); WriteByte(i+6,103); WriteByte(i+8,101); WriteByte(i+10,114); break; //Ranger
        case 1: WriteByte(j,80); WriteByte(i,80); WriteByte(i+2,105); WriteByte(i+4,114); WriteByte(i+6,97); WriteByte(i+8,116); WriteByte(i+10,101); break; //Pirate
        case 2: WriteByte(j,87); WriteByte(i,87); WriteByte(i+2,97); WriteByte(i+4,114); WriteByte(i+6,114); WriteByte(i+8,105); WriteByte(i+10,111); WriteByte(i+12,114); break; //Warrior
        case 3: WriteByte(j,84); WriteByte(i,84); WriteByte(i+2,114); WriteByte(i+4,97); WriteByte(i+6,110); WriteByte(i+8,115); WriteByte(i+10,112); WriteByte(i+12,111); WriteByte(i+14,114); WriteByte(i+16,116); break; //Transport
        case 4: WriteByte(j,76); WriteByte(i,76); WriteByte(i+2,105); WriteByte(i+4,110); WriteByte(i+6,101); WriteByte(i+8,114); break; //Liner
        case 5: WriteByte(j,68); WriteByte(i,68); WriteByte(i+2,105); WriteByte(i+4,112); WriteByte(i+6,108); WriteByte(i+8,111); WriteByte(i+10,109); WriteByte(i+12,97); WriteByte(i+14,116); break; //Diplomat
        }}

if (faction==5) {
    WriteByte(i,65); WriteByte(i+2,100); WriteByte(i+4,111); WriteByte(i+6,110); WriteByte(i+8,46); //Adon.
    switch(type) {
        case 1: WriteByte(i+10,49);WriteByte(j,49);break; //1 //Убийца
        case 2: WriteByte(i+10,50);WriteByte(j,50);break; //2 //Скала
        case 3: WriteByte(i+10,51);WriteByte(j,51);break; //3 //Болид
        case 4: WriteByte(i+10,65);WriteByte(j,65);break; //A //Быстрый
        case 5: WriteByte(i+10,66);WriteByte(j,66);break; //B //Неуязвимый
        case 6: WriteByte(i+10,67);WriteByte(j,67);break; //C //Ремонтный
        case 7: WriteByte(i+10,68);WriteByte(j,68);break; //D //Миоплазменный
        case 8: WriteByte(i+10,69);WriteByte(j,69);break; //E //Пигамарный
        }}

if (faction==6) {
  WriteByte(i,84); WriteByte(i+2,114); WriteByte(i+4,97); WriteByte(i+6,110); WriteByte(i+8,99);
  WriteByte(i+10,108); WriteByte(i+12,117); WriteByte(i+14,99); WriteByte(i+16,97); WriteByte(i+18,116);
  WriteByte(i+20,111); WriteByte(i+22,114); //Tranclucator
  WriteByte(j,84); WriteByte(j+2,114); WriteByte(j+4,97); WriteByte(j+6,110); WriteByte(j+8,99);
  WriteByte(j+10,108); WriteByte(j+12,117); WriteByte(j+14,99); WriteByte(j+16,97); WriteByte(j+18,116);
  WriteByte(j+20,111); WriteByte(j+22,114);
}

//ПРЕДУПРЕЖДЕНИЕ: привешивание обычному кораблю того, что что ниже - рандомно крушит игру,
// годно пока только для лулзов
if ((faction>6) and (faction<10)) { //dominators
    switch(faction) {
        case 7: WriteByte(i,66); WriteByte(i+2,108); WriteByte(i+4,97); WriteByte(i+6,122); WriteByte(i+8,101); WriteByte(i+10,114); WriteByte(i+12,46); WriteByte(i+14,66);
                WriteByte(j,66); WriteByte(j+2,108); WriteByte(j+4,97); WriteByte(j+6,122); WriteByte(j+8,101); WriteByte(j+10,114); break; //Blazer.
        case 8: WriteByte(i,75); WriteByte(i+2,101); WriteByte(i+4,108); WriteByte(i+6,108); WriteByte(i+8,101); WriteByte(i+10,114); WriteByte(i+12,46); WriteByte(i+14,75);
                WriteByte(j,75); WriteByte(j+2,101); WriteByte(j+4,108); WriteByte(j+6,108); WriteByte(j+8,101); WriteByte(j+10,114); break; //Keller.
        case 9: WriteByte(i,84); WriteByte(i+2,101); WriteByte(i+4,114); WriteByte(i+6,114); WriteByte(i+8,111); WriteByte(i+10,110); WriteByte(i+12,46); WriteByte(i+14,84);
                WriteByte(j,84); WriteByte(j+2,101); WriteByte(j+4,114); WriteByte(j+6,114); WriteByte(j+8,111); WriteByte(j+10,110); break; //Terron.
        }
    WriteByte(i+16,type+48); WriteByte(j+12,type+48); // 1..5 Эквентор, Ургант, Смерш, Менок, Штип
    }

if (faction==10) {WriteByte(i,88);WriteByte(i+2,46);WriteByte(i+4,47+type); //AB-ships X
                  WriteByte(j,120);WriteByte(j+2,47+type);}

if (faction==11) {WriteByte(i,72);WriteByte(i+2,83);WriteByte(i+4,46);WriteByte(i+6,47+type); //unknowns HS
                  WriteByte(j,72);WriteByte(j+2,83);WriteByte(j+4,47+type);}

i=0;
while (i<newsize2) {WriteByte(skin3+i*2,ReadLong(skin2+i*2));i=i+1;}
if (faction<11) {WriteLong(skin3+2*newsize2,115);} //s

return 0;}



long __stdcall ShipHaveArt(const long ship, const long type) //ShipHaveArt@8 //165
{long val=0;
long count=ShipArts(ship,0);
long i=0;
while (i<count) {i=i+1; if (ReadLong(ShipArts(ship,i)+12)==type){val=val+1;}}
return val;}

long __stdcall ShipHaveArtEquipped(const long ship, const long type) //ShipHaveArtEquipped@8 //166
{long val=0;
long count=ShipArts(ship,0);
long i=0; long art=0;
while (i<count) {i=i+1; art=ShipArts(ship,i); if ((ReadLong(art+12)==type) and (ReadLong(art+52)==1)){val=ReadByte(art+68);}}
return val;}



long __stdcall RepairShipEq(const long ship, const long amount, const long maxrepair) //RepairShipEq@12 //167
{  int i=2; int val=0; long item=0; long cond=0;
   while (i<14){item=ShipEqItems(ship,i); cond=GeneralEqProperty(item,4,-1); if (cond<maxrepair) {GeneralEqProperty(item,4,qMin(cond+amount,maxrepair));} if ((amount>0) and (cond==0)) {GeneralEqProperty(item,5,0); val=val+1;} i=i+1;}
   i=1; while (i<5){item=ShipEqArts(ship,i); cond=GeneralEqProperty(item,4,-1); if (cond<maxrepair) {GeneralEqProperty(item,4,qMin(cond+amount,maxrepair));} if ((amount>0) and (cond==0)) {GeneralEqProperty(item,5,0); val=val+1;} i=i+1;}
 return val;} // возвращает число предметов, которые были сломаны, а теперь функционируют


long __stdcall DamageShipEq(const long ship, const long amount, const long min) //DamageShipEq@12 //168
{  int i=2; int val=0; long item=0; long cond=0; long newcond=0;
   while (i<14){item=ShipEqItems(ship,i); cond=GeneralEqProperty(item,4,-1); if (cond>min) {newcond=qMax(cond-amount,min);if (newcond>0) {GeneralEqProperty(item,4,newcond);} else {GeneralEqProperty(item,4,0);GeneralEqProperty(item,5,1);val=val+1;}} i=i+1;}
   i=1; while (i<5){item=ShipEqArts(ship,i); cond=GeneralEqProperty(item,4,-1); if (cond>min) {newcond=qMax(cond-amount,min);if (newcond>0) {GeneralEqProperty(item,4,newcond);} else {GeneralEqProperty(item,4,0);GeneralEqProperty(item,5,1);val=val+1;}} i=i+1;}
 return val;} // возвращает число предметов, которые стали сломанными



long __stdcall ShipMissileAmmoCheck(const long ship, const long flag) //ShipMissileAmmoCheck@8 //169
{   long val=0; long i=1; long k=0; long item=0;// flag=0 - max ammo, flag<>0 - current ammo
    if (flag==0) {k=1;}
    while (i<6) {item=ShipEqItems(ship,8+i);
    if ((GeneralItemProperty(item,1,0)==50) or (GeneralItemProperty(item,1,0)==61)) {val=val+EqWeaponProperty(item,4+k,-1);} i=i+1;}
    return val;}

long __stdcall ShipMissileAmmoChange(const long ship, const long amount) //ShipMissileAmmoChange@8 //170
{   long i=0; long j=0; long temp=0; long item=0;
    long ammogain=qMax(qMin(ShipMissileAmmoCheck(ship,0)-ShipMissileAmmoCheck(ship,1),amount),i);
    long ammoloss=qMax(qMin(ShipMissileAmmoCheck(ship,1),-amount),i);
    long val=ammogain-ammoloss;

    while (ammogain>0) {
        i=1;temp=-1;while (i<6) {item=ShipEqItems(ship,8+i);
            if (((GeneralItemProperty(item,1,0)==50) or (GeneralItemProperty(item,1,0)==61))
                and ((EqWeaponProperty(item,4,-1))<temp) or (temp<0)){j=i;temp=EqWeaponProperty(item,4,-1);} i=i+1;}
        item=ShipEqItems(ship,8+j);
        EqWeaponProperty(item,4,EqWeaponProperty(item,4,-1)+1);ammogain=ammogain-1;}

    while (ammoloss>0) {
        i=1;temp=-1;while (i<6) {item=ShipEqItems(ship,8+i);
            if (((GeneralItemProperty(item,1,0)==50) or (GeneralItemProperty(item,1,0)==61))
                and (EqWeaponProperty(item,4,-1))>temp){j=i;temp=EqWeaponProperty(item,4,-1);} i=i+1;}
        item=ShipEqItems(ship,8+j);
        EqWeaponProperty(item,4,EqWeaponProperty(item,4,-1)-1);ammoloss=ammoloss-1;}
    return val;}



long __stdcall ShipMass(const long ship) //ShipMass@4 //171
{   long val=0; long itemcount=ShipItems(ship,0); long i=0;
    while (i<itemcount) {i=i+1;val=val+GeneralItemProperty(ShipItems(ship,i),3,0);}
    i=0;
    while (i<8) {val=val+ReadLong(ship+44+16*i);i=i+1;} //goods
    return val;}

long __stdcall ShipFreeSpace(const long ship) //ShipFreeSpace@4 //172
{   long val=2*GeneralItemProperty(ShipEqItems(ship,1),3,0); long itemcount=ShipItems(ship,0); long i=1;
    while (i<itemcount) {i=i+1;val=val-GeneralItemProperty(ShipItems(ship,i),3,0);}
    i=0;
    while (i<8) {val=val-ReadLong(ship+44+16*i);i=i+1;} //goods
    return val;}

//---------------------------------ship control----------------------------

long __stdcall ShipFlightPlan(const long ship,const long property, const long value) //ShipFlightPlan@12 //180
{long val=0;
switch (property){
        case 1: //flight status 1
        val=ReadLong(ship+840);
        if (value>-1) {WriteLong(ship+840,value);}
        break;
        case 2: //flight status 2
        val=ReadLong(ship+844);
        if (value>-1) {WriteLong(ship+844,value);}
        break;
        case 3: //target
        val=ReadLong(ship+848);
        if (value>0) {WriteLong(ship+848,value);}
        break;
        case 4: //coordx
        val=ReadLong(ship+852);
        if (!(value==0)) {WriteLong(ship+852,value);}// если нужно направить на звезду - ставьте 1,1 разница не заметна
        break;
        case 5: //coordy
        val=ReadLong(ship+856);
        if (!(value==0)) {WriteLong(ship+856,value);}
        break;}
 return val;}


long __stdcall OrderMove(const long ship,const long coordx,const long coordy) //OrderMove@12 //181
{WriteLong(ship+840,1);
 WriteLong(ship+844,2); //3? 5?
 WriteFloat(ship+852,coordx);WriteFloat(ship+856,coordy);
 return 0;}

long __stdcall OrderLand(const long ship,const long obj) //OrderLand@8 //182
{long objstar;long val=0;
 if (ReadLong(obj)==6465444) {objstar=PlanetToStar(obj);} else {objstar=ShipToStar(obj);}
 if (objstar==ShipToStar(ship)){
 WriteLong(ship+840,2);
 WriteLong(ship+844,2); //3? 5?
 WriteLong(ship+848,obj);
 val=1;}//success
 return val;}

long __stdcall OrderEnterHole(const long ship,const long hole) //OrderEnterHole@8 //183
{long val=0; long star1=ReadLong(hole+8); long star2=ReadLong(hole+20);
 if (star1==ShipToStar(ship)){WriteFloat(ship+852,ReadLong(hole+12));WriteFloat(ship+856,ReadLong(hole+16));val=1;}
 if (star2==ShipToStar(ship)){WriteFloat(ship+852,ReadLong(hole+24));WriteFloat(ship+856,ReadLong(hole+28));val=1;}
 if (val==1) {WriteLong(ship+840,4);
 WriteLong(ship+844,2); //3? 5?
 WriteLong(ship+848,hole);}
 return val;}

long __stdcall OrderLiftOff(const long ship) //OrderLand@4 //184
{long val=0;long flag=0;long count=0; long i=0; long star=0; long list=0;
 if ((ReadLong(ship+24)>0) or (ReadLong(ship+28)>0)){
 WriteLong(ship+840,5);
 WriteLong(ship+844,1); //3? 5?
 val=1;}//success
 if ((val==1) and (ReadByte(ship+12)==4)){//warrior
 star=ShipToStar(ship); list=ReadLong(star+48); count=ReadLong(list+8);
 while (i<count) {i=i+1; if (ReadLong(ReadLong(list+4)+(i-1)*4)==ship){flag=1;}}
 if (flag==0){AddObjectToList(list,ship);}}
 return val;}

long __stdcall OrderStop(const long ship) //OrderStop@4 //185
{WriteLong(ship+840,1);
 WriteLong(ship+844,2); //3? 5?
 WriteFloat(ship+852,CoordX(ship,0));WriteFloat(ship+856,CoordY(ship,0));
 return 0;}

long __stdcall OrderFollow(const long ship,const long ship2) //OrderFollow@8 //186
{long objstar;long val=0;
  if (ShipToStar(ship)==ShipToStar(ship2)){
 WriteLong(ship+840,6);
 WriteLong(ship+844,0);
 WriteLong(ship+848,ship);
 val=1;}//success
 return val;}

long __stdcall OrderAggroFollow(const long ship,const long ship2) //OrderAggroFollow@8 //187
{long objstar;long val=0;
 if (ShipToStar(ship)==ShipToStar(ship2)){
 WriteLong(ship+840,6);
 WriteLong(ship+844,1);
 WriteLong(ship+848,ship);
 val=1;}//success
 return val;}

long __stdcall OrderAttack(const long ship,const long obj, const long wnum) //OrderAttack@12 //188
{long weap=0; long i=1; //wnum=0 - all, wnum=-1 - all not already used
    while (i<6) {
        if ((wnum<1) or (i==wnum)){
            weap=ReadLong(ship+268+i*4);i=i+1; if (weap>0) {
                if ((Distance(ship,obj)>0) and (Distance(ship,obj)<ReadLong(weap+84))) {
                if ((wnum>-1) or (ReadLong(weap+92)==0)){WriteLong(weap+92,obj);}}}}
    i=i+1;}
return 0;}


// ship forsage



