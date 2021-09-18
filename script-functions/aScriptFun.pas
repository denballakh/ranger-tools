unit aScriptFun;

interface

uses EC_Expression;

procedure ScriptFunInit(va:TVarArrayEC);

implementation

uses SysUtils,Classes,Math,
     aMyFunction,Globals,GlobalsV,aItem,aConst,aGalaxy,aScript,aShip,aNormalShip,aPlayer,aRanger,aPlanet,aWarrior,aRuins,
     aKling,aPirate,aTransport,aEFilm,GR_Main,EC_Str,EC_Struct,fEquipmentShop,ab_Hit,ab_Ship,Robot,
     GI_MessageLoop,GI_GraphButton,GI_Label,GI_Image,GI_GI,GI_GAI,GI_GraphBuf,
     EC_BlockPar,ThreadCalc,aSaveLoad,fPanelLoad,SE_Process,SE_Space,SE_Ship2,SE_GAIEffect,
     SE_Ruins,SE_Planet,fStarMap,fShip2,fPanelMain, ab_ShipAI,ab_W,EC_Mem, aGalaxyEvent, aGalaxyStruct,
     Achievements,GI_XviD,MMSystem,aTranclucator,GI_MessageBox,fCount2,fCount1,fTextBox,fListBox,aMissile,aAsteroid,fTalk,fCustom,
     SE_Weapon,aEFilmEnd,aCalc,fGalaxy,GI_Edit,BreakMessageGIException;

procedure SF_GRun(av:array of TVarEC; code:TCodeEC);
begin
  GScriptGlobalRun:=true;
end;

procedure SF_GCntRun(av:array of TVarEC; code:TCodeEC);
var
  no:integer;
begin
  if High(av)<>1 then raise Exception.Create('Error.Script SF_GCntRun');

  no:=FindScriptTempl(av[1].VStr);
  if no<0 then raise Exception.Create('Error.Script.NotFound SF_GCntRun');

  av[0].VInt:=TScriptTemplUnit(GScriptTempl.Items[no]).FCntUse;
end;

procedure SF_GLastTurnRun(av:array of TVarEC; code:TCodeEC);
var
  no:integer;
begin
  if High(av)<1 then raise Exception.Create('Error.Script SF_GCntRun');

  no:=FindScriptTempl(av[1].VStr);
  if no<0 then raise Exception.Create('Error.Script.NotFound SF_GLastTurnRun');

  if (High(av)>=2) and (TScriptTemplUnit(GScriptTempl.Items[no]).FCntUse<1) then begin
    av[0].VInt:=av[2].VInt;
  end else begin
    av[0].VInt:=TScriptTemplUnit(GScriptTempl.Items[no]).FLastTurn;
  end;
end;

procedure SF_GAllCntRun(av:array of TVarEC; code:TCodeEC);
var
    cnt,zn,i:integer;
begin
  if High(av)>=1 then begin
    zn:=av[1].VInt;
    cnt:=0;
    for i:=0 to Galaxy.FScripts.Count-1 do begin
      if TScript(Galaxy.FScripts.Items[i]).FClass=zn then begin
        inc(cnt);
      end;
    end;
    av[0].VInt:=cnt;
  end else begin
    av[0].VInt:=Galaxy.FScripts.Count;
  end;
end;

procedure SF_IsScriptActive(av:array of TVarEC; code:TCodeEC);
var
  no:integer;
begin
  if High(av)<1 then raise Exception.Create('Error.Script IsScriptActive');

  av[0].VInt:=0;
  no:=FindScriptTempl(av[1].VStr);
  if no>=0 then av[0].VInt:=ord(TScriptTemplUnit(GScriptTempl.Items[no]).FRunScript >=0 );
  //IsScriptActive('MS_Begin');
end;

procedure SF_GetValueFromScript(av:array of TVarEC; code:TCodeEC);
var
  no,cnt:integer;
  scr:TScript;
  v:TVarEC;
begin
  cnt:=High(av);
  if cnt<2 then raise Exception.Create('Error.Script GetValueFromScript');

  if av[1].VStr='' then
  begin
    v:=GScriptFun.GetVarNE(av[2].VStr);
    if v=nil then raise Exception.Create('Error.Script GetValueFromScript - var '+av[2].VStr+' not found');

  end else begin
    no:=FindScriptTempl(av[1].VStr);
    if no<0 then exit;
    no:=TScriptTemplUnit(GScriptTempl.Items[no]).FRunScript;
    if no<0 then exit;
    scr:=Galaxy.FScripts[no];

    v:=scr.FCodeInit.LocalVar.GetVarNE(av[2].VStr);
    if v=nil then v:=scr.FCodeNextTurn.LocalVar.GetVarNE(av[2].VStr);
    if v=nil then v:=GScriptFun.GetVarNE(av[2].VStr);
    if v=nil then raise Exception.Create('Error.Script GetValueFromScript - var '+av[2].VStr+' not found in script '+av[1].VStr);
  end;

  no:=2;
  while (v.VType = vtArray) and (no<cnt) do
  begin
    inc(no);
    if av[no].VType = vtStr then v:=v.VArray.GetVar(av[no].VStr)
    else v:=v.VArray.Items[av[no].VInt];
  end;

  case v.VType of
    vtInt:   av[0].VInt:=v.VInt;
    vtDW:    av[0].VDW:=v.VDW;
    vtFloat: av[0].VFloat:=v.VFloat;
    vtStr:   av[0].VStr:=v.VStr;
    vtArray: av[0].VInt:=v.VArray.Count;
  end;
  //GetValueFromScript('MS_Begin','vSBId');
end;

procedure SF_GetVariableName(av:array of TVarEC; code:TCodeEC);
begin
  if High(av)<1 then raise Exception.Create('Error.Script GetVariableName');
  av[0].VStr:=av[1].Name;
end;

procedure SF_GetVariableType(av:array of TVarEC; code:TCodeEC);
begin
  if High(av)<1 then raise Exception.Create('Error.Script GetVariableType');
  av[0].VInt:=ord(av[1].VType);
end;

procedure SF_AddPlanetNews(av:array of TVarEC; code:TCodeEC);
begin
  if High(av)<1 then raise Exception.Create('Error.Script AddPlanetNews');

  if High(av)>1 then Galaxy.AddPlanetNews(TDifferentSituationInPlanet(av[2].VInt),av[1].VStr)
  else Galaxy.AddPlanetNews(dsGalaxyNews,av[1].VStr);
end;

procedure SF_AutoBattle(av:array of TVarEC; code:TCodeEC);
begin
  if High(av)<>1 then raise Exception.Create('Error.Script AutoBattle');

  AutoBattleShip:=TShip(av[1].VDW);
end;

procedure SF_GetOwner(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
  owner:integer;
begin
  if High(av)<>1 then raise Exception.Create('Error.Script SF_GetOwner');
  ship:=TShip(av[1].VDW);
  owner:=integer(ship.FOwner);

  av[0].VInt:=owner;
end;



procedure SF_GiveReward(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
  owner:TOwner;
  reward:TReward;
  number:integer;
  breward:PByte;
begin
  if(High(av) < 3) then raise Exception.Create('Error.Script SF_GiveReward');

  ship:=TShip(av[1].VDW);


  owner:=TOwner(av[2].Vint);
  reward:=TReward(av[3].Vint);//ForLiberationSystem, ForAccomplishment, ForSecretMission, ForCowardice, ForPerfidy, ForPlanetBattle
  number:=(ship as TRanger).RewardNumber(owner,[reward]);

  if(number = 255) then EError('Error RewardNumber=255');

  ship.AddReward(number);

end;

procedure SF_GiveRewardByNom(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SF_GiveRewardByNom');

  ship:=TShip(av[1].VDW);
  ship.AddReward(av[2].VInt);

end;

procedure SF_CountReward(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
  reward:TReward;
  i,cnt:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SF_CountReward');

  ship:=TShip(av[1].VDW);
  reward:=TReward(av[2].Vint);//ForLiberationSystem, ForAccomplishment, ForSecretMission, ForCowardice, ForPerfidy, ForPlanetBattle

  if ship.FRewards=nil then
  begin
    av[0].VInt:=0;
    exit;
  end;

  cnt:=0;
  for i:=0 to ship.FRewards.Count-1 do
    if SysToReward(CT('Reward.' + IntToStr(integer(ship.FRewards.Items[i])) + '.Type'))=reward then inc(cnt);

  av[0].VInt:=cnt;

end;

procedure SF_CountRewardByNom(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
  i,cnt,no:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SF_CountRewardByNom');

  ship:=TShip(av[1].VDW);
  no:=av[2].VInt;

  if ship.FRewards=nil then
  begin
    av[0].VInt:=0;
    exit;
  end;

  cnt:=0;
  for i:=0 to ship.FRewards.Count-1 do
    if integer(ship.FRewards.Items[i])=no then inc(cnt);

  av[0].VInt:=cnt;

end;

procedure SF_DeleteRewardByNom(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
  i,cnt,no:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SF_DeleteRewardByNom');

  ship:=TShip(av[1].VDW);
  no:=av[2].VInt;
  if High(av) > 2 then cnt:=av[3].VInt else cnt:=1;

  av[0].VInt:=0;

  if ship.FRewards=nil then exit;

  cnt:=0;
  for i:=ship.FRewards.Count-1 downto 0 do
    if integer(ship.FRewards.Items[i])=no then
    begin
      ship.FRewards.Delete(i);
      av[0].VInt:=av[0].VInt+1;
      if av[0].VInt >= cnt then exit;
    end;

end;


procedure SF_ShipPicksItem(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
  item:TItem;
  i,cnt,no:integer;
begin
  if High(av) < 2 then raise Exception.Create('Error.Script SF_ShipPicksItem');

  ship:=TShip(av[1].VDW);
  item:=TItem(av[2].VDW);

  if High(av)=2 then
  begin
    if ship.TakeItems_Test(item) then av[0].VInt:=1
    else if ship.RecentlyDroppedItem(item) then av[0].VInt:=-1
    else av[0].VInt:=0;
    exit;
  end;

  if av[3].VInt>0 then
  begin
    ship.TakeItems_Add(item);
    if ship.RecentlyDroppedItem(item) then
      ship.FRecentlyDroppedItems.Delete(ship.FRecentlyDroppedItems.IndexOf(item));
  end
  else if av[3].VInt<0 then
  begin
    ship.TakeItems_Del(item);
    ship.RecentlyDroppedItems_Add(item);
  end
  else
  begin
    ship.TakeItems_Del(item);
    if ship.RecentlyDroppedItem(item) then
      ship.FRecentlyDroppedItems.Delete(ship.FRecentlyDroppedItems.IndexOf(item));
  end;
end;


procedure SF_DropItem(av:array of TVarEC; code:TCodeEC);
label done;
var
  ship:TShip;
  eq:TEquipment;
  itemtype:TItemType;
  i:integer;
  found,nodropflag:boolean;
  ExlplotableState:boolean;
  sitem:TScriptItem;
begin
  found:=false;
  if High(av)<2 then raise Exception.Create('Error.Script SF_DropItem');

  ship:=TShip(av[1].VDW);

  if (av[2].VType = vtDW) and (av[2].VDW > 65536) then
  begin
    eq:=TEquipment(av[2].VDW);
    if High(av)>=3 then
    begin
      sitem:=TScriptItem(av[3].VDW);
      if sitem.FItem<>nil then sitem.FItem.FScriptItem:=nil;

      sitem.FItem:=eq;
      eq.FScriptItem:=sitem;
    end;

    nodropflag:=eq.FFlag_NoDrop;
      eq.FFlag_NoDrop:=false;
      ship.DropEx(eq);
      if ship.FCurStar.FItems.IndexOf(eq)>=0 then eq.FFlag_NoDrop:=nodropflag;

      found:=true;
      goto done;
  end;

  itemtype:=TItemType(av[2].VInt);
  ExlplotableState:=false;
  if High(av)>=3 then ExlplotableState:=boolean(av[3].VInt);

  for i:=0 to ship.FEquipments.Count-1 do begin
    eq:=ship.FEquipments.Items[i];
    if (eq.FItemType=itemtype) and (eq.FExplotable=ExlplotableState) then begin

      if High(av)>=4 then begin
        sitem:=TScriptItem(av[4].VDW);
        if sitem.FItem<>nil then sitem.FItem.FScriptItem:=nil;

        sitem.FItem:=eq;
        eq.FScriptItem:=sitem;
      end;

      nodropflag:=eq.FFlag_NoDrop;
      eq.FFlag_NoDrop:=false;
      ship.DropEx(eq);
      if ship.FCurStar.FItems.IndexOf(eq)>=0 then eq.FFlag_NoDrop:=nodropflag;

      found:=true;
      goto done;
    end;
  end;
  for i:=0 to ship.FArtefacts.Count-1 do begin
    eq:=ship.FArtefacts.Items[i];
    if (eq.FItemType=itemtype) and (eq.FExplotable=ExlplotableState) then begin

      if High(av)>=4 then begin
        sitem:=TScriptItem(av[4].VDW);
        if sitem.FItem<>nil then sitem.FItem.FScriptItem:=nil;

        sitem.FItem:=eq;
        eq.FScriptItem:=sitem;
      end;

      nodropflag:=eq.FFlag_NoDrop;
      eq.FFlag_NoDrop:=false;
      ship.DropEx(eq);
      if ship.FCurStar.FItems.IndexOf(eq)>=0 then eq.FFlag_NoDrop:=nodropflag;

      found:=true;
      goto done;
    end;
  end;

done:
  if not found then raise Exception.Create('Error.Script SF_DropItem - item not found');
end;

procedure SF_DropScriptItem(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
  sitem:TScriptItem;
  nodropflag:boolean;
begin
  if High(av)<>2 then raise Exception.Create('Error.Script DropScriptItem');

  ship:=TShip(av[1].VDW);
  sitem:=TScriptItem(av[2].VDW);
  if sitem.FItem=nil then Exit;
  if (ship.FEquipments.IndexOf(sitem.FItem)<0) and (ship.FArtefacts.IndexOf(sitem.FItem)<0) then Exit;
  if not ship.InNormalSpace then Exit;

  nodropflag:=sitem.FItem.FFlag_NoDrop;
  sitem.FItem.FFlag_NoDrop:=false;
  ship.DropEx(sitem.FItem);
  if sitem.FItem<>nil then sitem.FItem.FFlag_NoDrop:=nodropflag;
end;

procedure SF_DeleteEquipment(av:array of TVarEC; code:TCodeEC);
var
  i:integer;
  ship:TShip;
  eq:TEquipment;
  type_eq:TItemType;
begin
  if High(av)<>2 then raise Exception.Create('Error.Script SF_DeleteEquipment');

  ship:=TShip(av[1].VDW);

  i:=0;
  type_eq:=TItemType(av[2].VInt);

  while i<ship.FEquipments.Count do begin
    eq:=ship.FEquipments.Items[i];
    if (eq.FScriptItem=nil)and(eq.FItemType=type_eq) then begin
      ship.FEquipments.Delete(i);
      eq.Free;
    end else inc(i);
  end;

  ship.ArrangeEquipments;
  ship.CalcParam;
end;

procedure SF_Rnd(av:array of TVarEC; code:TCodeEC);
var
  min,max:integer;
begin
  if High(av)<2 then raise Exception.Create('Error.Script Rnd');

  if High(av)>2 then av[0].VInt:=Rnd(av[1].VInt,av[2].VInt,av[3].VDW)
  else if Galaxy<>nil then av[0].VInt:=RndOut(av[1].VInt,av[2].VInt,Galaxy.FRndOut)
  else begin
    min:=av[1].VInt;
    max:=av[2].VInt;
    av[0].VInt:=min+Random(max-min+1);
  end;
end;


procedure SF_GameDateTxtByTurn(av:array of TVarEC; code:TCodeEC);
begin
  if High(av)<>1 then raise Exception.Create('Error.Script GameDateTxtByTurn');

  av[0].VStr:=GameDateTxtG(av[1].VInt);
end;


procedure SF_StatusPlayer(av:array of TVarEC; code:TCodeEC);
begin
  case Player.Status of
    Trader: av[0].VInt:=1;
    Warrior: av[0].VInt:=0;
    Pirate: av[0].VInt:=-1;
  end;
end;

procedure SF_Id(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
begin
  if(High(av) <> 1) then raise Exception.Create('Error.Script SF_Id');

  obj:=TObject(av[1].VDW);

  if(obj is TShip) then begin
    av[0].VDW:=TShip(obj).FId;
  end else if(obj is TPlanet) then begin
    av[0].VDW:=TPlanet(obj).FId;
  end else if(obj is TStar) then begin
    av[0].VDW:=TStar(obj).FId;
  end else if(obj is TConstellation) then begin
    av[0].VDW:=TConstellation(obj).FId;
  end else if(obj is TItem) then begin
    av[0].VDW:=TItem(obj).FId;
  end else if(obj is THole) then begin
    av[0].VDW:=THole(obj).FId;
  end else if(obj is TMissile) then begin
    av[0].VDW:=TMissile(obj).FId;
  end else if(obj is TAsteroid) then begin
    av[0].VDW:=TAsteroid(obj).FId;
  end else raise Exception.Create('Error.Script SF_Id 2');
end;

procedure SF_GalaxyMoney(av:array of TVarEC; code:TCodeEC);
var
  own:TOwner;
begin
  if High(av)<1 then raise Exception.Create('Error.Script SF_GalaxyMoney');
  own:=People;
  if High(av)>=2 then begin
    case av[2].VInt of
      0: own:=Maloc;
      1: own:=Peleng;
      2: own:=People;
      3: own:=Fei;
      4: own:=Gaal;
      5: own:=Kling;
    else
      raise Exception.Create('Error.Script SF_GalaxyMoney');
    end;
  end;
  case av[1].VInt of
    0: av[0].VInt:=Galaxy.MiniMoney(own);
    1: av[0].VInt:=Galaxy.SmallMoney(own);
    2: av[0].VInt:=Galaxy.AverageMoney(own);
    3: av[0].VInt:=Galaxy.BigMoney(own);
    4: av[0].VInt:=Galaxy.HugeMoney(own);
  else
    raise Exception.Create('Error.Script SF_GalaxyMoney');
  end;
end;

procedure SF_SetName(av:array of TVarEC; code:TCodeEC);
var
  obj:TObject;
begin
  if High(av)<>2 then raise Exception.Create('Error.Script SF_SetName');
  obj:=TObject(av[1].VDW);
  if obj is TShip then TShip(obj).FName:=av[2].VStr
  else if obj is TPlanet then TPlanet(obj).FName:=av[2].VStr
  else if obj is TStar then TStar(obj).FName:=av[2].VStr
  else if obj is TItem then TItem(obj).FName:=av[2].VStr;
end;

procedure SF_UseTranclucator(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
  art:TArtefact;
  tart:TArtefactTranclucator;
  tran:TTranclucator;
  i:integer;
  angle:single;
begin
  if High(av)<1 then raise Exception.Create('Error.Script SF_UseTranclucator');

  av[0].VDW:=0;

  ship:=TShip(av[1].VDW);
  if ship.InHyperSpace then exit;

  art:=nil;
  if High(av)>1 then art:=TArtefact(av[2].VDW)
  else
  for i:=0 to ship.FArtefacts.Count-1 do
  begin
    art:=ship.FArtefacts.Items[i];
    if art is TArtefactTranclucator and not(art.FBroken) then break;
  end;
  if (art=nil) or not (art is TArtefactTranclucator) then exit;

  tart:= art as TArtefactTranclucator;
  tran:=TTranclucator(tart.FShip);


      tart.FShip := nil;
      tran.FCurStar := ship.FCurStar;
      ship.FCurStar.FShips.Add(tran);

      if ship.InNormalSpace then
      begin
        angle := Rnd(0, 360, ship.FCurStar.FRnd * Galaxy.FTurn * integer(tran.FId)) * pi / 180;
        tran.FPos.x := ship.FPos.x + sin(angle) * 100;
        tran.FPos.y := ship.FPos.y - cos(angle) * 100;
      end
      else
      if ship.FCurPlanet<>nil then tran.FCurPlanet:=ship.FCurPlanet
      else if ship.FCurShip<>nil then tran.FCurShip:=ship.FCurShip;

      tran.FGraphShip.Pos := tran.FPos;
      tran.FProprietor := ship;

      i:=ship.FArtefacts.IndexOf(tart);
      if i>=0 then ship.FArtefacts.Delete(i);
      i:=ship.FEquipments.IndexOf(tart);
      if i>=0 then ship.FEquipments.Delete(i);

      tart.Free;
      ship.CalcParam;

      tran.NextDay;
      //Player.FAchievementStats.CheckConditionAchTranclucators();

      av[0].VDW:=Cardinal(tran);

end;

procedure SF_HullDamage(av:array of TVarEC; code:TCodeEC);
var
  obj:TObject;
  hull:THull;
begin
  if High(av)<>1 then raise Exception.Create('Error.Script HullDamage');

  obj:=TObject(av[1].VDW);

  if obj is TShip then hull:=TShip(obj).FHull
  else if obj is TScriptItem then hull:=THull(TScriptItem(obj).FItem)
  else hull:=THull(obj);

  av[0].VInt:=100-Round((hull.FHitPoints/hull.FSize)*100);
end;

procedure SF_Hitpoints(av:array of TVarEC; code:TCodeEC);
var
  obj:TObject;
  hull:THull;
begin
  if High(av)<>1 then raise Exception.Create('Error.Script Hitpoints');

  obj:=TObject(av[1].VDW);

  if obj is TShip then hull:=TShip(obj).FHull
  else if obj is TScriptItem then hull:=THull(TScriptItem(obj).FItem)
  else hull:=THull(obj);

  av[0].VInt:=hull.FHitPoints;
end;

procedure SF_Hit(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
begin
  if High(av)<1 then ship:=GScriptCur.FCurShip
  else ship:=TShip(av[1].VDW);

  if ship=nil then Exit;

  with SctiptGetSS(ship,GScriptCur) do begin
    if High(av)<2 then begin
      av[0].VInt:=integer(FHit or FHitPlayer);
    end else if av[2].VInt<>0 then begin
      av[0].VInt:=integer(FHitPlayer);
    end else begin
      av[0].VInt:=integer(FHit);
    end;
  end;
  //changed
  //Hit(ship) - check if ship damaged player or player damaged ship (with weapon or explosion)
  //Hit(ship,1) - check if ship damaged player
  //Hit(ship,0) - check if player damaged ship
end;

procedure SF_ChangeGlobalRelationsShips(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
  obj:TObject;
  rct:TRelationChange;
  sst:TSetSShipType;
  so:TSetOwner;
begin
  if High(av)<>6 then raise Exception.Create('Error.Script ChangeGlobalRelationsShips');

  if av[1].VDW=0 then Exit;

  ship:=TShip(av[1].VDW);
  if (ship=nil) or (not (ship is TRanger)) then Exit;

  if (av[2].VDW>0) and (av[2].VDW<255) then obj:=TScriptConstellation(GScriptCur.FConstellation.Items[av[2].VDW]).FConstellation
  else if av[2].VDW<>0 then obj:=TObject(av[2].VDW)
  else obj:=nil;

  case av[3].VDW of
    0: rct:=RelationsToMin;
    1: rct:=RelationsToMax;
    2: rct:=RelationsPercentAdd;
    3: rct:=RelationsPercentDec;
  else
    rct:=RelationsToMin;
  end;

  sst:=TSetSShipType(Word(av[5].VDW));

  so:=TSetOwner(Byte(av[6].VDW));

  TRanger(ship).ChangeGlobalRelationsShips(obj,rct,av[4].VInt,sst,so);
end;

procedure SF_ChangeGlobalRelationsPlanets(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
  obj:TObject;
  rct:TRelationChange;
  so:TSetOwner;
begin
  if High(av)<>5 then raise Exception.Create('Error.Script ChangeGlobalRelationsPlanets');

  ship:=TShip(av[1].VDW);
  if (ship=nil) or (not (ship is TRanger)) then Exit;

  if (av[2].VDW>0) and (av[2].VDW<255) then obj:=TScriptConstellation(GScriptCur.FConstellation.Items[av[2].VDW]).FConstellation
  else if av[2].VDW<>0 then obj:=TObject(av[2].VDW)
  else obj:=nil;

  case av[3].VDW of
    0: rct:=RelationsToMin;
    1: rct:=RelationsToMax;
    2: rct:=RelationsPercentAdd;
    3: rct:=RelationsPercentDec;
  else
    rct:=RelationsToMin;
  end;

  so:=TSetOwner(Byte(av[5].VDW));

  TRanger(ship).ChangeGlobalRelationsPlanets(obj,rct,av[4].VInt,so);
end;

procedure SF_GlobalRelationsShips(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
  obj:TObject;
  sst:TSetSShipType;
  so:TSetOwner;
begin
  if High(av)<>4 then raise Exception.Create('Error.Script GlobalRelationsShips');

  ship:=TShip(av[1].VDW);
  if (ship=nil) or (not (ship is TRanger)) then Exit;

  if (av[2].VDW>0) and (av[2].VDW<255) then obj:=TScriptConstellation(GScriptCur.FConstellation.Items[av[2].VDW]).FConstellation
  else if av[2].VDW<>0 then obj:=TObject(av[2].VDW)
  else obj:=nil;

  sst:=TSetSShipType(Word(av[3].VDW));

  so:=TSetOwner(Byte(av[4].VDW));

  av[0].VInt:=TRanger(ship).GlobalRelationsShips(obj,sst,so);
end;

procedure SF_GlobalRelationsPlanets(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
    obj:TObject;
    so:TSetOwner;
begin
    if High(av)<>3 then raise Exception.Create('Error.Script GlobalRelationsPlanets');

    ship:=TShip(av[1].VDW);
    if (ship=nil) or (not (ship is TRanger)) then Exit;

    if (av[2].VDW>0) and (av[2].VDW<255) then obj:=TScriptConstellation(GScriptCur.FConstellation.Items[av[2].VDW]).FConstellation
    else if av[2].VDW<>0 then obj:=TObject(av[2].VDW)
    else obj:=nil;

    so:=TSetOwner(Byte(av[3].VDW));

    av[0].VInt:=TRanger(ship).GlobalRelationsPlanets(obj,so);
end;

procedure SF_SetRelationGroup(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>3 then raise Exception.Create('Error.Script SetRelationGroup');

    GScriptCur.SetRelationGroup(av[1].VInt,av[2].VInt,TRelationType(av[3].VInt));
end;

procedure SF_SetRelationPlanet(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>3 then raise Exception.Create('Error.Script SetRelationPlanet');

    GScriptCur.SetRelationPlanet(av[2].VInt,TPlanet(av[1].VDW),TRelationType(av[3].VInt));
end;

procedure SF_GetRelationPlanet(av:array of TVarEC; code:TCodeEC);
var
	planet:TPlanet;
begin
    if High(av)<>2 then raise Exception.Create('Error.Script GetRelationPlanet');

    planet:=TPlanet(av[1].VDW);
    av[0].VDW:=planet.RelationToShip(TShip(av[2].VDW));
end;

procedure SF_CurTurn(av:array of TVarEC; code:TCodeEC);
begin
    av[0].VInt:=Galaxy.FTurn;
    if High(av)>0 then Galaxy.FTurn:=av[1].VInt;
end;

procedure SF_ShipType(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
begin
    if High(av)<1 then raise Exception.Create('Error.Script ShipType');
    ship:=TShip(av[1].VDW);

    if ship.FCustomTypeName<>'' then av[0].VStr:=ship.FCustomTypeName
    else if (ship.FScriptShip<>nil) and
            (TScriptShip(ship.FScriptShip).FScript.FCD = 'Script.PC_fem_rangers') and
            (TScriptShip(ship.FScriptShip).GetOGroup.FName='GroupFem') then av[0].VStr:='FemRanger'
    else av[0].VStr:=ship.TypeName;



    if High(av)>1 then
    begin
      if av[2].VStr=ship.TypeName then ship.FCustomTypeName:=''
      else ship.FCustomTypeName:=av[2].VStr;
    end;
end;

procedure SF_ConName(av:array of TVarEC; code:TCodeEC);
var
    con:TConstellation;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ConName');
    if av[1].VDW < Cardinal(Galaxy.FConstellation.Count) then con:=Galaxy.FConstellation[av[1].VDW]
    else con:=TConstellation(av[1].VDW);
    av[0].VStr:=con.Name;
end;

procedure SF_StarName(av:array of TVarEC; code:TCodeEC);
var
    star:TStar;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script StarName');
    star:=TStar(av[1].VDW);
    av[0].VStr:=star.FName;
end;

procedure SF_StarMapLabel(av:array of TVarEC; code:TCodeEC);
var
    star:TStar;
begin
    if High(av)<1 then raise Exception.Create('Error.Script StarMapLabel');
    star:=TStar(av[1].VDW);
    av[0].VStr:=star.FMapLabel;
    if High(av)>1 then star.FMapLabel:=av[2].VStr;
end;

procedure SF_PlanetName(av:array of TVarEC; code:TCodeEC);
var
    planet:TPlanet;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script PlanetName');
    planet:=TPlanet(av[1].VDW);
    av[0].VStr:=planet.FName;
end;

procedure SF_IdToPlanet(av:array of TVarEC; code:TCodeEC);
var
	planet:TPlanet;
begin
	if High(av)<>1 then raise Exception.Create('Error.Script IdToPlanet');
    av[0].VDW:=Cardinal(Galaxy.IdToPlanet(av[1].VDW));
end;

procedure SF_IdToShip(av:array of TVarEC; code:TCodeEC);
var
	ship:TShip;
begin
  if High(av)<>1 then raise Exception.Create('Error.Script IdToShip');
  av[0].VDW:=Cardinal(Galaxy.IdToShip(av[1].VDW, false));
end;

procedure SF_IdToItem(av:array of TVarEC; code:TCodeEC);
var
	ship:TShip;
begin
  if High(av)<>1 then raise Exception.Create('Error.Script IdToItem');
  av[0].VDW:=Cardinal(Galaxy.IdToItem(av[1].VDW, false));
end;

procedure SF_PlanetSetGoods(av:array of TVarEC; code:TCodeEC);
var
    it:tItemType;
begin
    if High(av)<>3 then raise Exception.Create('Error.Script PlanetSetGoods');
    it:=TItemType(av[2].VInt);
    TPlanet(av[1].VDW).FShopGoods[it].Cnt:=av[3].VInt;
end;

procedure SF_ShipName(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipName');
    ship:=TShip(av[1].VDW);
    av[0].VStr:=ship.Name;
end;

procedure SF_ShipRank(av:array of TVarEC; code:TCodeEC);
var
    ship:TNormalShip;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipRank');
    ship:=TShip(av[1].VDW) as TNormalShip;
    av[0].VInt:=integer(ship.FRank);
end;

procedure SF_ShipRankPoints(av:array of TVarEC; code:TCodeEC);
var
    ship:TNormalShip;
begin
    if High(av)<1 then raise Exception.Create('Error.Script ShipRankPoints');
    ship:=TShip(av[1].VDW) as TNormalShip;
    av[0].VInt:=integer(ship.FRankPoints);
    if High(av)>1 then ship.FRankPoints:=word(av[2].VInt);
end;

procedure SF_ShipNextRankPoints(av:array of TVarEC; code:TCodeEC);
var
    ship:TNormalShip;
begin
    if High(av)<1 then raise Exception.Create('Error.Script ShipNextRankPoints');
    ship:=TShip(av[1].VDW) as TNormalShip;
    av[0].VInt:=integer(mRank[ship.FRank]);
end;

procedure SF_ShipRaiseRank(av:array of TVarEC; code:TCodeEC);
var
    ship:TNormalShip;
begin
    if High(av)<1 then raise Exception.Create('Error.Script ShipRaiseRank');
    ship:=TShip(av[1].VDW) as TNormalShip;
    ship.GetNewRank;
end;

procedure SF_ShipStar(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipStar');
    ship:=TShip(av[1].VDW);
    av[0].VDW:=Cardinal(ship.FCurStar);
end;

procedure SF_StarToCon(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script StarToCon');
    av[0].VDW:=Cardinal(TStar(av[1].VDW).FConstellation);
end;

procedure SF_ConNear(av:array of TVarEC; code:TCodeEC);
var
    i,cnt,u,cntu:integer;
    con,cc,cc2:TConstellation;
begin
    if High(av)<2 then raise Exception.Create('Error.Script ConNear');
    con:=TConstellation(av[1].VDW);

    cnt:=con.FConstellations.Count;
    cntu:=High(av)-1;
    for i:=0 to cnt-1 do begin
        cc:=con.FConstellations.Items[i];
        for u:=0 to cntu-1 do begin
            cc2:=TConstellation(av[2+u].VDW);
            if cc=cc2 then begin
                av[0].VInt:=1;
                Exit;
            end;
        end;
    end;
    av[0].VInt:=0;
end;

procedure SF_ConStars(av:array of TVarEC; code:TCodeEC);
var
    con:TConstellation;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ConStars');
    con:=TConstellation(av[1].VDW);
    av[0].VInt:=con.FStars.Count;
end;

procedure SF_ConStar(av:array of TVarEC; code:TCodeEC);
var
    con:TConstellation;
    no:integer;
begin
    if High(av)<>2 then raise Exception.Create('Error.Script ConStar');
    con:=TConstellation(av[1].VDW);
    no:=av[2].VInt;
    if (no<0) or (no>=con.FStars.Count) then begin av[0].VDW:=0; Exit; end;
    av[0].VDW:=Cardinal(con.FStars.Items[no]);
end;

procedure SF_GalaxyStars(av:array of TVarEC; code:TCodeEC);
begin
    av[0].VInt:=Galaxy.FStars.Count;
end;

procedure SF_GalaxyStar(av:array of TVarEC; code:TCodeEC);
var
    no:integer;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script GalaxyStar');
    no:=av[1].VInt;
    if (no<0) or (no>=Galaxy.FStars.Count) then begin av[0].VDW:=0; Exit; end;
    av[0].VDW:=Cardinal(Galaxy.FStars.Items[no]);
end;

procedure SF_StarAngleBetween(av:array of TVarEC; code:TCodeEC);
var
    star1,star2,star3:TStar;
    mina,maxa,ca:single;
begin
    if High(av)<>5 then raise Exception.Create('Error.Script StarAngleBetween');
    star1:=TStar(av[1].VDW);
    star2:=TStar(av[2].VDW);
    star3:=TStar(av[3].VDW);
    mina:=av[4].VFloat;
    maxa:=av[5].VFloat;
    ca:=abs(AngleDist(AngleCalc(star2.FPos,star1.FPos),AngleCalc(star2.FPos,star3.FPos)));
    if (ca>=mina) and (ca<=maxa) then av[0].VInt:=1
    else av[0].VInt:=0;
end;

procedure SF_FindPlanet(av:array of TVarEC; code:TCodeEC);
var
    star:TStar;
    pla:TPlanet;
    str,tstr:WideString;
    dstart,dend:single;
    i,cnt,u,cntu:integer;
    li:TList;
begin
    if High(av)<>4 then raise Exception.Create('Error.Script FindPlanet');
    star:=TStar(av[1].VDW);
    str:=av[2].VStr;
    dstart:=av[3].VFloat/100;
    dend:=av[4].VFloat/100;

    li:=TList.Create;

    cnt:=star.FPlanets.Count;
    cntu:=GetCountParEC(str,',');
    for i:=0 to cnt-1 do begin
        pla:=star.FPlanets.Items[i];
        for u:=0 to cntu-1 do begin
            tstr:=GetStrParEC(str,u,',');
            if (tstr='NotMaloc') and (pla.FOwner=Maloc) then break
            else if (tstr='NotPeleng') and (pla.FOwner=Peleng) then break
            else if (tstr='NotPeople') and (pla.FOwner=People) then break
            else if (tstr='NotFei') and (pla.FOwner=Fei) then break
            else if (tstr='NotGaal') and (pla.FOwner=Gaal) then break
            else if (tstr='NotKling') and (pla.FOwner=Kling) then break
            else if (tstr='NotPirateClan') and (pla.FOwner=PirateClan) then break
            else if (tstr='NotNone') and (pla.FOwner=None) then break
        end;
        if u<cntu then continue;
        li.Add(pla);
    end;

    if li.Count<1 then begin av[0].VDW:=0; li.Free; exit; end;
    i:=Round((li.Count-1)*dstart);
    u:=Round((li.Count-1)*dend);
    i:=i+Rnd(0,(u-i),Galaxy.FTurn*Galaxy.FRnd);

    av[0].VDW:=Cardinal(li.Items[i]);

    li.Free;
end;



procedure SF_ShipCanJump(av:array of TVarEC; code:TCodeEC);
var
    star1,star2:TStar;
    i,cnt,range,fuel,d:integer;
    checkFuel:boolean;
    ship:TShip;
begin
    if High(av)<3 then raise Exception.Create('Error.Script CanJump');
    ship:=TShip(av[1].VDW);

    av[0].VInt:=0;
    if (ship.FFuelTanks=nil) or (ship.FEngine=nil) then Exit;
    range:=ship.GiperJumpInTheory;

    cnt:=High(av)-1;
    fuel:=0; checkFuel:=false;
    if (av[cnt+1].VType = vtInt) and (av[cnt+1].VInt = 1) then
    begin
      checkFuel:=true;
      fuel:=ship.FFuelTanks.FFuel;
      cnt:=cnt-1;
    end;

    for i:=2 to cnt do begin
        star1:=TStar(av[i].VDW);
        star2:=TStar(av[i+1].VDW);

        d:=round(Dist(star2.FPos,star1.FPos));

        if checkFuel then
        begin
          range:=min(range,fuel);
          fuel:=fuel-d;
        end;
        if d>range then Exit;
    end;
    av[0].VInt:=1;
end;

procedure SF_ShipInStar(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>2 then raise Exception.Create('Error.Script ShipInStar');
    if (av[1].VDW<>0) and (TShip(av[1].VDW).FCurStar=TStar(av[2].VDW)) then av[0].VInt:=1 else av[0].VInt:=0;
end;

procedure SF_ShipInPlanet(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>2 then raise Exception.Create('Error.Script ShipInPlanet');
    if TShip(av[1].VDW).FCurPlanet=TPlanet(av[2].VDW) then av[0].VInt:=1 else av[0].VInt:=0;
end;

procedure SF_ShipStatistic(av:array of TVarEC; code:TCodeEC);
var
	obj: TObject;
  ship: TNormalShip;
  i:integer;
begin
  if (High(av) < 2) then raise Exception.Create('Error.Script ShipStatistic');

  obj:=TShip(av[1].VDW);
  if(obj is TNormalShip) then ship:=TNormalShip(obj)
  else raise Exception.Create('Error.Script ShipStatistic - illegal object type');

  case av[2].VInt of
    0: begin
      av[0].VInt:=ship.FStatistic.KillAllShip;
      if(High(av) > 2) then ship.FStatistic.KillAllShip:=av[3].VInt;
    end;
    1: begin
      av[0].VInt:=ship.FStatistic.KillPirate;
      if(High(av) > 2) then ship.FStatistic.KillPirate:=av[3].VInt;
    end;
    2: begin
      av[0].VInt:=ship.FStatistic.KillDominator;
      if(High(av) > 2) then ship.FStatistic.KillDominator:=av[3].VInt;
    end;
    3: begin
      av[0].VInt:=ship.FStatistic.LiberationSystem;
      if(High(av) > 2) then ship.FStatistic.LiberationSystem:=av[3].VInt;
    end;
    4: begin
      av[0].VInt:=ship.FStatistic.KillPacific;
      if(High(av) > 2) then ship.FStatistic.KillPacific:=av[3].VInt;
    end;
    5: begin
      av[0].VInt:=ship.FStatistic.KillWarrior;
      if(High(av) > 2) then ship.FStatistic.KillWarrior:=av[3].VInt;
    end;
    6: begin
      av[0].VInt:=ship.FStatistic.KillRangers;
      if(High(av) > 2) then ship.FStatistic.KillRangers:=av[3].VInt;
    end;
    7: begin
      if ship<>Player then exit;
      av[0].VInt:=Player.FKillShipInHole;
      if(High(av) > 2) then Player.FKillShipInHole:=av[3].VInt;
    end;
    8: begin
      if ship<>Player then exit;
      av[0].VInt:=Player.FKillShipInGiperSpace;
      if(High(av) > 2) then Player.FKillShipInGiperSpace:=av[3].VInt;
    end;
    9: begin
      if ship<>Player then exit;
      av[0].VInt:=Player.FTradePenalty;
      if(High(av) > 2) then Player.FTradePenalty:=av[3].VInt;
    end;
    10: begin
      av[0].VDW:=cardinal(ship.FHomePlanet);
      if(High(av) > 2) then
      begin
        if ship is TWarrior then
        begin
          i:=ship.FHomePlanet.FWarriors.IndexOf(ship);
          if i>=0 then ship.FHomePlanet.FWarriors.Delete(i);
          TPlanet(av[3].VDW).FWarriors.Add(ship);
        end;
        ship.FHomePlanet:=TPlanet(av[3].VDW);
      end;
    end;
    11: begin
      av[0].VInt:=ship.FDay;
      if(High(av) > 2) then ship.FDay:=av[3].VInt;
    end;
  else
    raise Exception.Create('Error.Script ShipStatistic');
  end;
end;

procedure SF_PlayerDominatorStatistic(av:array of TVarEC; code:TCodeEC);
begin
  if High(av)<1 then raise Exception.Create('Error.Script PlayerDominatorStatistic');
  av[0].VInt:=Player.FKillDominatorsByType[TKlingType(av[1].VInt)];
  if High(av)>1 then Player.FKillDominatorsByType[TKlingType(av[1].VInt)]:=av[2].VInt;
end;

procedure SF_ShipMoney(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
begin
    if High(av)<1 then raise Exception.Create('Error.Script ShipMoney');
    ship:=TShip(av[1].VDW);
    av[0].VInt:=ship.SMoney;
    if High(av)>=2 then begin
        ship.SMoney:=max(0,av[2].VInt);
    end;
end;

procedure SF_ShipFuel(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
begin
    if High(av)<1 then raise Exception.Create('Error.Script ShipFuel');
    ship:=TShip(av[1].VDW);
    if (ship=nil) or (ship.FFuelTanks=nil) then av[0].VInt:=0
    else av[0].VInt:=ship.FFuelTanks.FFuel;
    if (High(av)>=2) and (ship.FFuelTanks<>nil) then begin
        ship.FFuelTanks.FFuel:=av[2].VInt;
        if ship.FFuelTanks.FFuel<0 then ship.FFuelTanks.FFuel:=0;
    end;
end;

procedure SF_ShipFuelLow(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipFuelLow');
    ship:=TShip(av[1].VDW);
    if ship.FFuelTanks=nil then av[0].VInt:=1
    else if ship.FFuelTanks.FFuel<(ship.FFuelTanks.FCapacity) then av[0].VInt:=1
    else av[0].VInt:=0;
end;

procedure SF_ShipStrengthInBestRanger(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipStrengthInBestRanger');

    ship:=TShip(av[1].VDW);

    av[0].VFloat:=ship.FStrengthInBestRanger;
end;

procedure SF_ShipStrengthInAverageRanger(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipStrength');

    ship:=TShip(av[1].VDW);

    av[0].VFloat:=ship.FStrength/Galaxy.FRangersAverageStrength;
end;


procedure SF_ChanceToWin(av:array of TVarEC; code:TCodeEC);
var
    ship1,ship2:TShip;
begin
    if High(av)<2 then raise Exception.Create('Error.Script ChanceToWin');

    ship1:=TShip(av[1].VDW);
    ship2:=TShip(av[2].VDW);

    if (high(av)>2) and (av[3].VInt<>0) then av[0].VFloat:=ship1.ChanceToWin(ship2)
    else av[0].VInt:=ship1.ChanceToWinInPercent(ship2);
end;

procedure SF_RangerStatus(av:array of TVarEC; code:TCodeEC);
var
    ship:TObject;
begin
    if High(av)<1 then raise Exception.Create('Error.Script RangerStatus');
    ship:=TObject(av[1].VDW);

    if High(av)>1 then
    begin
      if      av[2].VStr='EminentWarrior' then av[0].VInt:=ord(ship=Galaxy.FEminentRangers[Warrior])
      else if av[2].VStr='EminentTrader'  then av[0].VInt:=ord(ship=Galaxy.FEminentRangers[Trader])
      else if av[2].VStr='EminentPirate'  then av[0].VInt:=ord(ship=Galaxy.FEminentRangers[Pirate])
      else raise Exception.Create('Error.Script RangerStatus - unknown keyword '+av[2].VStr);
      exit;
    end;

    if not (ship is TRanger) then raise Exception.Create('Error.Script RangerStatus 2');

    av[0].VInt:=integer((ship as TRanger).Status);
end;

procedure SF_RangerPlaceInRating(av:array of TVarEC; code:TCodeEC);
var
    ship:TObject;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script RangerPlaceInRating');
    ship:=TObject(av[1].VDW);
    if not (ship is TRanger) then raise Exception.Create('Error.Script RangerPlaceInRating 2');
    av[0].VInt:=(ship as TRanger).FRating;
end;

procedure SF_RangerExcludedFromRating(av:array of TVarEC; code:TCodeEC);
var
    ship:TObject;
    ranger:TRanger;
begin
    if High(av)<1 then raise Exception.Create('Error.Script RangerExcludedFromRating');
    ship:=TObject(av[1].VDW);
    if not (ship is TRanger) then raise Exception.Create('Error.Script RangerExcludedFromRating 2');
    ranger:=TRanger(ship);
    av[0].VInt:=ord(ranger.FExcludedFromRating);
    if High(av)>1 then
    begin
      ranger.FExcludedFromRating := (av[2].VInt<>0);
      if ranger.FExcludedFromRating then
      begin
        if Galaxy.FEminentRangers[Trader] = ranger then Galaxy.FEminentRangers[Trader]:=nil;
        if Galaxy.FEminentRangers[Pirate] = ranger then Galaxy.FEminentRangers[Pirate]:=nil;
        if Galaxy.FEminentRangers[Warrior] = ranger then Galaxy.FEminentRangers[Warrior]:=nil;
      end;
    end;
end;

procedure SF_ShipFind(av:array of TVarEC; code:TCodeEC);
var
	st:TShipType;
    star:TStar;
    ship:TShip;
    i:integer;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipFind');

    av[0].VDW:=0;
    if Player=nil then Exit;

    st:=TShipType(av[1].VInt);
    star:=Player.FCurStar;

    for i:=0 to star.FShips.Count-1 do begin
    	ship:=star.FShips.Items[i];
        if ship.FShipType=st then begin
	        av[0].VDW:=Cardinal(ship);
            Exit;
        end;
    end;
end;

procedure SF_ShipDestroy(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<1 then raise Exception.Create('Error.Script ShipDestroy');

    if TShip(av[1].VDW)=nil then Exit;

    if High(av)<=1 then begin
	    TShip(av[1].VDW).FShipDestroy:=true;
    end else begin
	    TShip(av[1].VDW).FShipDestroy:=boolean(av[2].VInt);
    end;
end;

procedure SF_ShipDestroyType(av:array of TVarEC; code:TCodeEC);
var
	i,u:integer;
    star:TStar;
    ship:TShip;
    st:integer;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipDestroyType');

    st:=av[1].VInt;

	for i:=0 to Galaxy.FStars.Count-1 do
  begin
    star:=Galaxy.FStars.Items[i];
		for u:=0 to star.FShips.Count-1 do
    begin
      ship:=star.FShips.Items[u];
      if (st=1) and (ship.FShipType=t_Kling) and (TKling(ship).FSeries=t_Blazer) and (TKling(ship).FType<>KlingBoss)
         and not ship.IsCustomFaction then ship.FShipDestroy:=true;
    end;
  end;
end;


procedure SF_ItemDestroy(av:array of TVarEC; code:TCodeEC);
var
  item: TItem;
  obj: TObject;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemDestroy');
  obj:=TObject(av[1].VDW);
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TItem(TScriptItem(obj).FItem);
  if(item <> nil) then
  begin
    av[0].VInt:=item.FItemDestroy;
    if High(av) > 1 then item.FItemDestroy:=av[2].VInt;
//0 - default
//1 - item will explode, 2 - item will explode and deal quark bomb damage, x>2 item will explode and deal x damage
//0 after OnItemHit - item will not produce explosion effect on destruction
//-x item will resist x weapon/missile/explosion hits
  end;
end;

procedure SF_RangersCapital(av:array of TVarEC; code:TCodeEC);
begin
    av[0].VInt:=Galaxy.FRangersAverageCapital;
end;


procedure SF_GroupToShip(av:array of TVarEC; code:TCodeEC);
var
    cnt:integer;
    sship:TScriptShip;
    i,no:integer;
    ship:TShip;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script GroupToShip');

    no:=av[1].VInt;

    ship:=nil;
    cnt:=GScriptCur.FShips.Count;
    for i:=0 to cnt-1 do begin
        sship:=GScriptCur.FShips.Items[i];
        if sship.FGroup=no then begin
            ship:=sship.FShip;
            if ship<>Player then begin
                av[0].VDW:=Cardinal(ship);
                Exit;
            end;
        end;
    end;
    av[0].VDW:=Cardinal(ship);
end;

procedure SF_OrderJump(av:array of TVarEC; code:TCodeEC);
var
  ab: boolean;
  scriptorder: byte;
  ship: TShip;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script OrderJump');

  ab:=false;
  if High(av)>=3 then ab:=boolean(av[3].VInt);

  ship:=TShip(av[1].VDW);
  if(ship <> nil) then
  begin
    scriptorder:=ship.FScriptOrderAbsolute;
    ship.FScriptOrderAbsolute:=0;
    ship.OrderJump(TStar(av[2].VDW),ab);
    ship.FScriptOrderAbsolute:=scriptorder;

    if ship=Player then AutoBattleShip:=nil;

    if (ship=Player) and (GetCurrentML = GFormStarMap) and (GFormStarMap.FMode = fsmm_Control) then
    begin
      GFormStarMap.ShipPathHide;
      GFormStarMap.ShipPathShow(ship);
    end;

  end;
end;

procedure SF_OrderLanding(av:array of TVarEC; code:TCodeEC);
var
  ab: boolean;
  scriptorder: byte;
  ship: TShip;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script OrderLanding');

  ab:=false;
  if(High(av) >= 3) then ab:=boolean(av[3].VInt);

  ship:=TShip(av[1].VDW);
  if(ship <> nil) then
  begin
    scriptorder:=ship.FScriptOrderAbsolute;
    ship.FScriptOrderAbsolute:=0;
    ship.OrderLanding(TObject(av[2].VDW), ab);
    ship.FScriptOrderAbsolute:=scriptorder;

    if ship=Player then AutoBattleShip:=nil;

    if (ship=Player) and (GetCurrentML = GFormStarMap) and (GFormStarMap.FMode = fsmm_Control) then
    begin
      GFormStarMap.ShipPathHide;
      GFormStarMap.ShipPathShow(ship);
    end;
  end;
end;





procedure SF_IsPlayer(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script IsPlayer');
    ship:=TShip(av[1].VDW);
    av[0].VInt:=integer(ship=Player);
end;

procedure SF_GroupCount(av:array of TVarEC; code:TCodeEC);
var
    sship:TScriptShip;
    i,cnt,no,cntingroup:integer;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script GroupCount');

    no:=av[1].VInt;
    cntingroup:=0;

    cnt:=GScriptCur.FShips.Count;
    for i:=0 to cnt-1 do begin
        sship:=GScriptCur.FShips.Items[i];
        if sship.FGroup=no then inc(cntingroup);
    end;

    av[0].VInt:=cntingroup;
end;



procedure SF_GroupIn(av:array of TVarEC; code:TCodeEC);
var
    nogroup:integer;
    obj:TObject;
    i,cnt:integer;
    sship:TScriptShip;
begin
    if High(av)<>2 then raise Exception.Create('Error.Script GroupIn');
    nogroup:=av[1].VInt;
    obj:=TObject(av[2].VDW);

    if obj is TConstellation then begin
        cnt:=GScriptCur.FShips.Count;
        for i:=0 to cnt-1 do begin
            sship:=GScriptCur.FShips.Items[i];
            if (sship.FGroup=nogroup) and (sship.FShip.FCurStar.FConstellation<>obj) then begin av[0].VInt:=0; Exit; end;
        end;
    end else if obj is TStar then begin
        cnt:=GScriptCur.FShips.Count;
        for i:=0 to cnt-1 do begin
            sship:=GScriptCur.FShips.Items[i];
            if (sship.FGroup=nogroup) and (sship.FShip.FCurStar<>obj) then begin av[0].VInt:=0; Exit; end;
        end;
    end else if obj is TPlanet then begin
        cnt:=GScriptCur.FShips.Count;
        for i:=0 to cnt-1 do begin
            sship:=GScriptCur.FShips.Items[i];
            if (sship.FGroup=nogroup) and (sship.FShip=Player) and (Player.FCaptainOnTheBridge<>0) then
            begin
              if (Player.FBridgeCurPlanet=obj) then continue;
              av[0].VInt:=0;
              Exit;
            end;
            if (sship.FGroup=nogroup) and ((not sship.FShip.InPlanet) or (sship.FShip.FCurPlanet<>obj)) then begin av[0].VInt:=0; Exit; end;
        end;
    end else if obj is TShip then begin
        cnt:=GScriptCur.FShips.Count;
        for i:=0 to cnt-1 do begin
            sship:=GScriptCur.FShips.Items[i];
            if (sship.FGroup=nogroup) and (sship.FShip=Player) and (Player.FCaptainOnTheBridge<>0) then
            begin
              if (Player.FBridgeCurShip=obj) then continue;
              av[0].VInt:=0;
              Exit;
            end;
            if (sship.FGroup=nogroup) and ((not sship.FShip.InShip) or (sship.FShip.FCurShip<>obj)) then begin av[0].VInt:=0; Exit; end;
        end;
    end else if obj is TScriptPlace then begin
        cnt:=GScriptCur.FShips.Count;
        for i:=0 to cnt-1 do begin
            sship:=GScriptCur.FShips.Items[i];
            if (sship.FGroup=nogroup) and (not TScriptPlace(obj).ShipInPlace(sship.FShip)) then begin av[0].VInt:=0; Exit; end;
        end;
    end;

    av[0].VInt:=1;
end;

procedure SF_CountIn(av:array of TVarEC; code:TCodeEC);
var
    nogroup:integer;
    obj:TObject;
    i,cnt,cis:integer;
    sship:TScriptShip;
    skipHyper:boolean;
begin
    if High(av)<1 then raise Exception.Create('Error.Script CountIn');
    nogroup:=av[1].VInt;

    skipHyper:=(High(av)>1) and (av[2].VInt<>0);

    cis:=0;
    if High(av)=1 then
    begin
        cnt:=GScriptCur.FShips.Count;
        for i:=0 to cnt-1 do
        begin
            sship:=GScriptCur.FShips.Items[i];
            if (sship.FGroup=nogroup) then inc(cis);
        end;
    end else begin
        obj:=TObject(av[2].VDW);

        if obj is TConstellation then
        begin
            cnt:=GScriptCur.FShips.Count;
            for i:=0 to cnt-1 do
            begin
                sship:=GScriptCur.FShips.Items[i];
                if skipHyper and sship.FShip.InHyperSpace then continue;
                if (sship.FGroup=nogroup) and (sship.FShip.FCurStar.FConstellation=obj) then inc(cis);
            end;
        end else if obj is TStar then
        begin
            cnt:=GScriptCur.FShips.Count;
            for i:=0 to cnt-1 do
            begin
                sship:=GScriptCur.FShips.Items[i];
                if skipHyper and sship.FShip.InHyperSpace then continue;
                if (sship.FGroup=nogroup) and (sship.FShip.FCurStar=obj) then inc(cis);
            end;
        end else if obj is TPlanet then
        begin
            cnt:=GScriptCur.FShips.Count;
            for i:=0 to cnt-1 do
            begin
                sship:=GScriptCur.FShips.Items[i];
                if (sship.FGroup=nogroup) and (sship.FShip=Player) and (Player.FCaptainOnTheBridge<>0) and (Player.FBridgeCurPlanet=obj) then begin inc(cis); continue; end;
                if (sship.FGroup=nogroup) and ((sship.FShip.InPlanet) and (sship.FShip.FCurPlanet=obj)) then inc(cis);
            end;
        end else if obj is TShip then
        begin
            cnt:=GScriptCur.FShips.Count;
            for i:=0 to cnt-1 do
            begin
                sship:=GScriptCur.FShips.Items[i];
                if (sship.FGroup=nogroup) and (sship.FShip=Player) and (Player.FCaptainOnTheBridge<>0) and (Player.FBridgeCurShip=obj) then begin inc(cis); continue; end;
                if (sship.FGroup=nogroup) and ((sship.FShip.InShip) and (sship.FShip.FCurShip=obj)) then inc(cis);
            end;
        end else if obj is TScriptPlace then
        begin
            cnt:=GScriptCur.FShips.Count;
            for i:=0 to cnt-1 do
            begin
                sship:=GScriptCur.FShips.Items[i];
                if (sship.FGroup=nogroup) and (TScriptPlace(obj).ShipInPlace(sship.FShip)) then inc(cis);
            end;
        end;
    end;

    av[0].VInt:=cis;
end;







procedure SF_NearestGroup(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
    sship:TScriptShip;
    i,cnt,u,cntu,nogr:integer;
    tdist,mindist:single;
begin
    if High(av)<3 then raise Exception.Create('Error.Script NearestGroup');
    ship:=TShip(av[1].VDW);

    nogr:=av[2].VInt;
    mindist:=1e15;

    cnt:=GScriptCur.FShips.Count;
    cntu:=High(av)-1;
    for i:=0 to cnt-1 do begin
        sship:=GScriptCur.FShips.Items[i];
        for u:=0 to cntu-1 do if sship.FGroup=av[2+u].VInt then break;
        if (u<cntu) and (sship.FShip.FCurStar=ship.FCurStar) and (sship.FShip.InNormalSpace) then begin
            tdist:=Dist2(ship.FPos,sship.FShip.FPos);
            if tdist<mindist then begin mindist:=tdist; nogr:=sship.FGroup; end;
        end;
    end;

    av[0].VInt:=nogr;
end;

procedure SF_ChangeState(av:array of TVarEC; code:TCodeEC);
var cship:Cardinal;
    ship:TShip;
    v1,v2:TVarEC;
    no,i,es:integer;
begin
    if High(av)<1 then raise Exception.Create('Error.Script ChangeState');

    if av[1].VType<>vtStr then no:=av[1].VInt
    else begin
      for no:=0 to GScriptCur.FState.Count-1 do
        if TScriptState(GScriptCur.FState[no]).FName = av[1].VStr then break;

      if no>=GScriptCur.FState.Count then raise Exception.Create('Error.Script ChangeState '+av[1].VStr);
    end;

    v1:=GScriptCur.FCodeInit.LocalVar.GetVar('CurShip');
    v2:=GScriptCur.FCodeInit.LocalVar.GetVar('EndState');
    cship:=v1.VDW;
    es:=v2.VInt;

    if High(av)>=2 then ship:=TShip(av[2].VDW) else ship:=GScriptCur.FCurShip;
    GScriptCur.ChangeState(SctiptGetSS(ship,GScriptCur),no);

    v1.VDW:=cship;
    v2.VInt:=es;
    GScriptCur.FCurShip:=TShip(cship);
end;



procedure SF_StarAngle(av:array of TVarEC; code:TCodeEC);
var
    star1,star2:TStar;
begin
    if High(av)<>2 then raise Exception.Create('Error.Script StarAngle');
    star1:=TStar(av[1].VDW);
    star2:=TStar(av[2].VDW);

    av[0].VFloat:=AngleCalc(star1.FPos,star2.FPos);
end;

procedure SF_NewsAdd(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script NewsAdd');
    MsgPlayerAdd(mp_Galaxy,Galaxy.FTurn,av[1].VStr);
end;

procedure SF_MsgAdd(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
    sship:TScriptShip;
    nogroup,i,cnt:integer;
begin
    if High(av)<>2 then raise Exception.Create('Error.Script NewsAdd');

    ship:=nil;
    nogroup:=av[2].VInt;
    cnt:=GScriptCur.FShips.Count;
    for i:=0 to cnt-1 do begin
        sship:=GScriptCur.FShips.Items[i];
        if sship.FGroup=nogroup then begin ship:=sship.FShip; break; end;
    end;
    if (ship=nil) or Player.InHyperSpace or (Player.FCurStar<>ship.FCurStar) then begin av[0].VInt:=0; exit; end;
    with MsgPlayerAdd(mp_Ether,Galaxy.FTurn,av[1].VStr) do begin
        FObjShip1:=ship.FId;
    end;
    av[0].VInt:=1;
end;

procedure SF_Ether(av:array of TVarEC; code:TCodeEC);
var
    obj:TObject;
    sameStar:boolean;
    tstr:WideString;
    mpt:TMessagePlayerType;
begin
    if High(av)<3 then raise Exception.Create('Error.Script Ether');
    av[0].VInt:=0;

    mpt:=TMessagePlayerType(av[1].VInt);
    tstr:=av[2].VStr;

    obj:=nil; sameStar:=false;
    if High(av)>=4 then
    begin
        obj:=TObject(av[4].VDW);
        if obj=nil then exit;
        if obj is TShip then begin if TShip(obj).InNormalSpace and Player.InNormalSpace then sameStar:=(TShip(obj).FCurStar=Player.FCurStar); end
        else if obj is TPlanet then begin if Player.InNormalSpace then sameStar:=(TPlanet(obj).FStar=Player.FCurStar); end
        else Exception.Create('Error.Script Ether objtype');
    end;

    if (mpt<>mp_Quest) and (mpt<>mp_QuestOk) and (mpt<>mp_QuestCancel) then
    begin
        if (tstr<>'') and (GScriptCur<>nil) and (GScriptCur.FUniqueEther.Find(tstr)>=0) then Exit;
        if (obj<>nil) and not sameStar then Exit;
        if GScriptCur<>nil then GScriptCur.FUniqueEther.Add(tstr,0);
    end;

    if (mpt=mp_Quest) and (tstr<>'') and (GScriptCur<>nil) then GScriptCur.FEtherId.Add(tstr);

    with MsgPlayerAdd(mpt,Galaxy.FTurn,StringReplaceEC(StringReplaceEC(av[3].VStr, '<clr>', clr), '<clrEnd>', clrEnd),tstr) do
    begin
        if obj<>nil then
        begin
          if obj is TShip then FObjShip1:=TShip(obj).FId
          else FObjPlanet1:=TPlanet(obj).FId;
        end;

        if (High(av)>=5) then obj:=TObject(av[5].VDW) else obj:=nil;
        if obj<>nil then
        begin
          if obj is TShip then FObjShip2:=TShip(obj).FId
          else FObjPlanet2:=TPlanet(obj).FId;
        end;

        if (High(av)>=6) then obj:=TObject(av[6].VDW) else obj:=nil;
        if obj<>nil then
        begin
          if obj is TShip then FObjShip3:=TShip(obj).FId
          else FObjPlanet3:=TPlanet(obj).FId;
        end;
    end;

    av[0].VInt:=1;
end;

procedure SF_CustomEther(av:array of TVarEC; code:TCodeEC);
var
    obj:TObject;
    sameStar:boolean;
    tstr:WideString;
    mpt:TMessagePlayerType;
begin
    if High(av)<3 then raise Exception.Create('Error.Script Ether');
    av[0].VInt:=0;

    mpt:=TMessagePlayerType(av[2].VInt);
    tstr:=av[3].VStr;

    obj:=nil; sameStar:=false;
    if High(av)>=5 then
    begin
        obj:=TObject(av[5].VDW);
        if obj=nil then exit;
        if obj is TShip then begin if TShip(obj).InNormalSpace and Player.InNormalSpace then sameStar:=(TShip(obj).FCurStar=Player.FCurStar); end
        else if obj is TPlanet then begin if Player.InNormalSpace then sameStar:=(TPlanet(obj).FStar=Player.FCurStar); end
        else Exception.Create('Error.Script Ether objtype');
    end;

    if (mpt<>mp_Quest) and (mpt<>mp_QuestOk) and (mpt<>mp_QuestCancel) then
    begin
        if (tstr<>'') and (GScriptCur<>nil) and (GScriptCur.FUniqueEther.Find(tstr)>=0) then Exit;
        if (obj<>nil) and not sameStar then Exit;
        if GScriptCur<>nil then GScriptCur.FUniqueEther.Add(tstr,0);
    end;

    if (mpt=mp_Quest) and (tstr<>'') and (GScriptCur<>nil) then GScriptCur.FEtherId.Add(tstr);


    with MsgPlayerAdd(mpt,Galaxy.FTurn,StringReplaceEC(StringReplaceEC(av[4].VStr, '<clr>', clr), '<clrEnd>', clrEnd),tstr) do
    begin
        FCustomType:=av[1].VStr;

        if obj<>nil then
        begin
          if obj is TShip then FObjShip1:=TShip(obj).FId
          else FObjPlanet1:=TPlanet(obj).FId;
        end;

        if (High(av)>=6) then obj:=TObject(av[6].VDW) else obj:=nil;
        if obj<>nil then
        begin
          if obj is TShip then FObjShip2:=TShip(obj).FId
          else FObjPlanet2:=TPlanet(obj).FId;
        end;

        if (High(av)>=7) then obj:=TObject(av[7].VDW) else obj:=nil;
        if obj<>nil then
        begin
          if obj is TShip then FObjShip3:=TShip(obj).FId
          else FObjPlanet3:=TPlanet(obj).FId;
        end;
    end;
    av[0].VInt:=1;
end;

procedure SF_EtherDelete(av:array of TVarEC; code:TCodeEC);
begin
	if High(av)<>1 then raise Exception.Create('Error.Script EtherDelete');
	MsgPlayerDelById(av[1].VStr);//delete by key
end;

procedure SF_EtherIdAdd(av:array of TVarEC; code:TCodeEC);
begin
	if High(av)<>1 then raise Exception.Create('Error.Script EtherIdAdd');
  GScriptCur.FEtherId.Add(av[1].VStr);
end;

procedure SF_EtherIdDelete(av:array of TVarEC; code:TCodeEC);
var
	i:integer;
begin
	if High(av)<>1 then raise Exception.Create('Error.Script EtherIdDelete');

    while true do begin
    i:=GScriptCur.FEtherId.Find(av[1].VStr);
        if i>=0 then GScriptCur.FEtherId.Delete(i)
        else break;
    end;
end;

procedure SF_EtherState(av:array of TVarEC; code:TCodeEC);
var
	mp:TMessagePlayer;
begin
    if High(av)<1 then raise Exception.Create('Error.Script EtherState');

    mp:=MsgPlayerFindId(av[1].VStr);
    if mp=nil then begin av[0].VInt:=-1; Exit; end;

    av[0].VInt:=integer(mp.FType);
end;

procedure SF_ConChangeRelationToRanger(av:array of TVarEC; code:TCodeEC);
var
    ship:TRanger;
    con:TConstellation;
    zn:integer;
    star:TStar;
    pla:TPlanet;
    i,u,cnt,cntu:integer;
begin
    if High(av)<>3 then raise Exception.Create('Error.Script ConChangeRelationToRanger');
    con:=TConstellation(av[1].VDW);
    ship:=TRanger(av[2].VDW);
    zn:=av[3].VInt;

    cnt:=con.FStars.Count;
    for i:=0 to cnt-1 do begin
        star:=con.FStars.Items[i];
        cntu:=star.FPlanets.Count;
        for u:=0 to cntu-1 do begin
            pla:=star.FPlanets.Items[u];
            if pla.FOwner=None then continue;
            pla.ChangeRelationToRanger(ship,zn);
        end;
    end;
end;

procedure SF_GetData(av:array of TVarEC; code:TCodeEC);
var
    no:integer;
    ship:TShip;
begin
    no:=0;

    if High(av)>=1 then no:=av[1].VInt;
    if High(av)>=2 then
    begin
      ship:=TShip(av[2].VDW);
      if (ship=Player) and (GScriptCur=nil) then exit;
    end else begin
      ship:=GScriptCur.FCurShip;
    end;

    if ship=Player then av[0].VDW:=SctiptGetSS(ship,GScriptCur).FData[no]
    else av[0].VDW:=TScriptShip(ship.FScriptShip).FData[no];
end;

procedure SF_SetData(av:array of TVarEC; code:TCodeEC);
var
    no:integer;
    ship:TShip;
begin
    if High(av)<1 then raise Exception.Create('Error.Script SetData');
    no:=0;

    if High(av)>=2 then no:=av[2].VInt;
    if High(av)>=3 then
    begin
      ship:=TShip(av[3].VDW);
      if (ship=Player) and (GScriptCur=nil) then exit;
    end else begin
      ship:=GScriptCur.FCurShip;
    end;

    if ship=Player then SctiptGetSS(ship,GScriptCur).FData[no]:=av[1].VDW
    else TScriptShip(ship.FScriptShip).FData[no]:=av[1].VDW;
end;

procedure SF_ShipData(av:array of TVarEC; code:TCodeEC);
begin
    av[0].VDW:=SctiptGetSS(GScriptCur.FCurShip,GScriptCur).FData[0];
    if High(av)>=1 then begin
        SctiptGetSS(GScriptCur.FCurShip,GScriptCur).FData[0]:=av[1].VDW;
    end;
end;

procedure SF_Format(av:array of TVarEC; code:TCodeEC);
var
    tstr,clr:WideString;
    i,cnt:integer;
begin
    if High(av)<1 then raise Exception.Create('Error.Script Format');

    tstr:=av[1].VStr;
    cnt:=(High(av)-1) div 2;

    if High(av)>2*cnt+1 then
    begin
      clr:=av[High(av)].VStr;
      if clr<>'' then clr:='<color='+clr+'>';
    end else clr:=txtStandart;


    for i:=0 to cnt-1 do begin
        tstr:=StringReplaceEC(tstr,av[2+i*2+0].VStr,ColorStr(av[2+i*2+1].VStr,clr{txtStandart}));
    end;

    av[0].VStr:=tstr;
end;

procedure SF_DeleteTags(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<1 then raise Exception.Create('Error.Script DeleteTags');
    av[0].VStr:=TagDeleteEC(av[1].VStr);
end;

procedure SF_Dialog(av:array of TVarEC; code:TCodeEC);
var
    i,cnt,u,cntu:integer;
    groupno:Cardinal;
    sship:TScriptShip;
    mainThread:boolean;
begin
    if High(av)<1 then raise Exception.Create('Error.Script Dialog');
    av[0].VInt:=0;
    if GR_Exit or (Player=nil) or ((High(av)=1) and (av[1].VDW=0)) or not Player.InNormalSpace or (GFormCur <> mlf_StarMap) then exit;
    if GetCurrentML = GFormTalk then exit;
    mainThread:=CP_State in [0,2,4,6];

    if High(av)=1 then
    begin
      if mainThread then
      begin
        GTalk_FShip:=TShip(av[1].VDW);
        GTalk_FComputer:=false;
        GTalk_ScriptRun:=-1;
        GFormStarMap.TalkLoop;
        av[0].VInt:=1;
      end else begin
        if TShip(av[1].VDW).TalkPlayer(false) then av[0].VInt:=1;
      end;
      exit;
    end;

    cnt:=High(av)+1-2;
    for i:=0 to cnt-1 do
    begin
        groupno:=av[2+i].VDW;
        if groupno<65536 then
        begin
            cntu:=GScriptCur.FShips.Count;
            for u:=0 to cntu-1 do
            begin
                sship:=GScriptCur.FShips.Items[u];
                if (sship.FGroup=integer(groupno)) and (sship.FShip<>Player) then
                begin
                    GTalk_ScriptRun:=-1;
                    GScriptCur.CallDialog(av[1].VInt);
                    if GTalk_ScriptRun>=0 then
                    begin
                        if mainThread then
                        begin
                          GTalk_FShip:=sship.FShip;
                          GTalk_FComputer:=false;
                          GFormStarMap.TalkLoop;
                          av[0].VInt:=1;
                        end else begin
                          if sship.FShip.TalkPlayer(false) then av[0].VInt:=1;
                        end;
                        exit;
                    end;
                end;
            end;
        end else if TObject(groupno) is TShip then
        begin
            GTalk_ScriptRun:=-1;
            GScriptCur.CallDialog(av[1].VInt);
            if GTalk_ScriptRun>=0 then
            begin
                if mainThread then
                begin
                  GTalk_FShip:=TShip(groupno);
                  GTalk_FComputer:=false;
                  GFormStarMap.TalkLoop;
                  av[0].VInt:=1;
                end else begin
                  if TShip(groupno).TalkPlayer(false) then av[0].VInt:=1;
                end;
                exit;
            end;
        end else if TObject(groupno) is TPlanet then
        begin
            GTalk_ScriptRun:=-1;
            GScriptCur.CallDialog(av[1].VInt);
            if GTalk_ScriptRun>=0 then
            begin
                if TPlanet(groupno).TalkPlayer() then
                begin
                    av[0].VInt:=1;
                    exit;
                end;
            end;
        end;
    end;
end;

procedure SF_DText(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script DText');

  if Player.InShip then begin
    GFormRuinsTalk.Text:=StringReplaceEC(StringReplaceEC(av[1].VStr, '<clr>', clr), '<clrEnd>', clrEnd);
  end else if not Player.InPlanet then begin
    GFormTalk.Text:=StringReplaceEC(StringReplaceEC(av[1].VStr, '<clr>', clr), '<clrEnd>', clrEnd);
  end else begin
    GFormGov.Text:=StringReplaceEC(StringReplaceEC(av[1].VStr, '<clr>', clr), '<clrEnd>', clrEnd);
  end;
end;


procedure SF_DAddText(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script DAddText');
  if Player.InShip then begin
    GFormRuinsTalk.Text:=GFormRuinsTalk.Text+StringReplaceEC(StringReplaceEC(av[1].VStr, '<clr>', clr), '<clrEnd>', clrEnd);
  end else if not Player.InPlanet then begin
    GFormTalk.Text:=GFormTalk.Text+StringReplaceEC(StringReplaceEC(av[1].VStr, '<clr>', clr), '<clrEnd>', clrEnd);
  end else begin
    GFormGov.Text:=GFormGov.Text+StringReplaceEC(StringReplaceEC(av[1].VStr, '<clr>', clr), '<clrEnd>', clrEnd);
  end;
end;


procedure SF_DAdd(av:array of TVarEC; code:TCodeEC);
begin
  if High(av)<>1 then raise Exception.Create('Error.Script DAdd');
  GScriptCur.CallDialogAnswerAnswer(av[1].VInt);
end;

procedure SF_DAnswer(av:array of TVarEC; code:TCodeEC);
var
  cnt:integer;
begin
    if(High(av) < 1) then raise Exception.Create('Error.Script DAnswer');

    if Player.InShip then begin
        if GetStrParEC(LowerCase(av[1].VStr),0,'~')='takeoff' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormRuinsTalk.M_ScriptTakeOff(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormRuinsTalk.M_ScriptTakeOff('');
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='exit' then begin
            //GFormRuinsTalk.M_ScriptContinue;
            if Player.FCaptainOnTheBridge>0 then Player.ExitBridge else GFormRuinsTalk.M_ScriptContinue;
        end else if (LowerCase(av[1].VStr)='main') then begin
            //GFormRuinsTalk.M_ScriptContinue;
            GFormRuinsTalk.M_Main(false);
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='exit_news' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormRuinsTalk.M_ScriptToNews(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormRuinsTalk.M_ScriptToNews('');
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='exit_end' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormRuinsTalk.M_ScriptToEnd(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormRuinsTalk.M_ScriptToEnd('');
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='hangar' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormRuinsTalk.M_ScriptToHangar(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormRuinsTalk.M_ScriptToHangar('');
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='restart' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormRuinsTalk.M_DialogRestart(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormRuinsTalk.M_DialogRestart('');
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='goods' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormRuinsTalk.M_ScriptToGoods(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormRuinsTalk.M_ScriptToGoods('');
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='block' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormRuinsTalk.A_Add('- '+GetStrParEC(av[1].VStr,1,cnt-1,'~'),g_TalkEmpty,0);
            end else begin
                GFormRuinsTalk.A_Add('',g_TalkEmpty,0);
            end;
        end else begin
            GFormRuinsTalk.A_Add('- '+av[1].VStr,GFormRuinsTalk.I_Script,GScriptCur.FCurAnswer);
        end;
    end else if not Player.InPlanet then begin
        if (GetStrParEC(LowerCase(av[1].VStr),0,'~')='exit') or
           (GetStrParEC(LowerCase(av[1].VStr),0,'~')='takeoff') then
        begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormTalk.M_ScriptExit(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormTalk.M_ScriptExit('');
            end;
        end else if (GetStrParEC(LowerCase(av[1].VStr),0,'~')='fastexit') then
        begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormTalk.A_Add('- '+GetStrParEC(av[1].VStr,1,cnt-1,'~'),GFormTalk.I_Exit,0);
            end else begin
                GFormTalk.A_Add('',GFormTalk.I_Exit,0);
            end;
        end else if (LowerCase(av[1].VStr)='main') then begin
            //GFormTalk.M_ScriptMain;
            //GFormTalk.M_Main(false);
            GTalk_ScriptRun:=-1;
            GFormTalk.I_Start(true);

        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='exit_end' then begin
            GEndType:=4;
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormTalk.M_ScriptExit(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormTalk.M_ScriptExit('');
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='restart' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormTalk.M_DialogRestart(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormTalk.M_DialogRestart('');
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='block' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormTalk.A_Add('- '+GetStrParEC(av[1].VStr,1,cnt-1,'~'),g_TalkEmpty,0);
            end else begin
                GFormTalk.A_Add('',g_TalkEmpty,0);
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='snap' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormTalk.A_Add('- '+GetStrParEC(av[1].VStr,1,cnt-1,'~'),GFormTalk.I_ScriptSnap,GScriptCur.FCurAnswer);
            end else begin
                GFormTalk.A_Add('',GFormTalk.I_ScriptSnap,GScriptCur.FCurAnswer);
            end;
        end else begin
            GFormTalk.A_Add('- '+av[1].VStr,GFormTalk.I_Script,GScriptCur.FCurAnswer);
        end;
    end else begin
        if GetStrParEC(LowerCase(av[1].VStr),0,'~')='takeoff' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormGov.M_ScriptTakeOff(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormGov.M_ScriptTakeOff('');
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='planet' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormGov.M_ScriptPlanet(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormGov.M_ScriptPlanet('');
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='goods' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormGov.M_ScriptGoods(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormGov.M_ScriptGoods('');
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='shop' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormGov.M_ScriptShop(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormGov.M_ScriptShop('');
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='hangar' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormGov.M_ScriptHangar(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormGov.M_ScriptHangar('');
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='restart' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormGov.M_DialogRestart(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormGov.M_DialogRestart('');
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='exit_news' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormGov.M_ScriptNews(GetStrParEC(av[1].VStr,1,cnt-1,'~'));
            end else begin
                GFormGov.M_ScriptNews('');
            end;
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='exit' then begin
            GFormGov.M_ScriptContinue;
        end else if (LowerCase(av[1].VStr)='main') then begin
            //GFormGov.M_ScriptContinue;
            GFormGov.M_Main(false);
        end else if GetStrParEC(LowerCase(av[1].VStr),0,'~')='block' then begin
            cnt:=GetCountParEC(av[1].VStr,'~');
            if cnt>1 then begin
                GFormGov.A_Add('- '+GetStrParEC(av[1].VStr,1,cnt-1,'~'),g_TalkEmpty,0);
            end else begin
                GFormGov.A_Add('',g_TalkEmpty,0);
            end;
        end else begin
            GFormGov.A_Add('- '+av[1].VStr,GFormGov.I_Script,GScriptCur.FCurAnswer);
        end;
    end;
end;

procedure SF_DChange(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script DChange');
    GTalk_ScriptRun:=av[1].VInt;
end;

procedure SF_Player(av:array of TVarEC; code:TCodeEC);
begin
    av[0].VDW:=Cardinal(Player);
end;

procedure SF_ItemExist(av:array of TVarEC; code:TCodeEC);
var
    sitem:TScriptItem;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ItemExist');

    sitem:=TScriptItem(av[1].VDW);

    if sitem.FItem=nil then begin
        av[0].VInt:=0;
        Exit;
    end;

    av[0].VInt:=1;
end;

procedure SF_ItemIn(av:array of TVarEC; code:TCodeEC);
var
    star:TStar;
    ship:TShip;
    planet:TPlanet;
    obj:TObject;
    sitem:TScriptItem;
    sship:TScriptShip;
    i:integer;
begin
    if High(av)<>2 then raise Exception.Create('Error.Script ItemInStar');

    sitem:=TScriptItem(av[1].VDW);

    if sitem.FItem=nil then begin
        av[0].VInt:=0;
        Exit;
    end;

    obj:=TObject(av[2].VDW);

    if cardinal(obj)<65536 then begin
        for i:=0 to GScriptCur.FShips.Count-1 do begin
            sship:=GScriptCur.FShips.Items[i];
            if sship.FGroup <> integer(obj) then continue;
            if (sship.FShip.FEquipments.IndexOf(sitem.FItem)>0) or (sship.FShip.FArtefacts.IndexOf(sitem.FItem)>0) then begin
                av[0].VInt:=1;
                Exit;
            end;
        end;
        av[0].VInt:=0;

    end else if obj is TStar then begin
        star:=obj as TStar;

        if star.FItems.IndexOf(sitem.FItem)<0 then av[0].VInt:=0
        else av[0].VInt:=1;

    end else if obj is TShip then begin
        ship:=obj as TShip;

        if (ship.FEquipments.IndexOf(sitem.FItem)<0) and (ship.FArtefacts.IndexOf(sitem.FItem)<0) then av[0].VInt:=0
        else av[0].VInt:=1;

    end else if obj is TPlanet then begin
    	planet:=obj as TPlanet;

        if (Player.FCurPlanet=planet) and (GShopList<>nil) then begin
        	if ShopListFind(sitem.FItem)=nil then av[0].VInt:=0
    	    else av[0].VInt:=1;
        end else begin
	        if planet.FEquipmentShop.IndexOf(sitem.FItem)<0 then av[0].VInt:=0
    	    else av[0].VInt:=1;
        end;

    end;
end;


procedure SF_ItemCount(av:array of TVarEC; code:TCodeEC);
var
	it:TItemType;
    ship:TShip;
    i,cnt:integer;
begin
    if High(av)<>2 then raise Exception.Create('Error.Script SF_ItemCount');

    ship:=TShip(av[1].VDW);
    it:=TItemType(av[2].VInt);

    cnt:=0;
    for i:=0 to ship.FEquipments.Count-1 do begin
    	if TItem(ship.FEquipments.Items[i]).FItemType=it then inc(cnt);
    end;
    for i:=0 to ship.FArtefacts.Count-1 do begin
    	if TItem(ship.FArtefacts.Items[i]).FItemType=it then inc(cnt);
    end;

    av[0].VInt:=cnt;
end;

procedure SF_DecayGoods(av:array of TVarEC; code:TCodeEC);
var
    it:tItemType;
    obj:TObject;
begin
    if High(av)<>2 then raise Exception.Create('Error.Script DecayGoods');

    it:=TItemType(av[2].VInt);

	obj:=TPlanet(av[1].VDW);
    if obj is TPlanet then (obj as TPlanet).DecayGoods(True,[it]);
end;

procedure SF_UpsurgeGoods(av:array of TVarEC; code:TCodeEC);
var
    it:tItemType;
begin
    if High(av)<>2 then raise Exception.Create('Error.Script DecayGoods');

    it:=TItemType(av[2].VInt);

    TPlanet(av[1].VDW).UpsurgeGoods(True,[it]);
end;

procedure SF_GoodsAdd(av:array of TVarEC; code:TCodeEC);
var
    it:tItemType;
    obj:TObject;
begin
    if High(av)<>3 then raise Exception.Create('Error.Script GoodsAdd');

    it:=TItemType(av[2].VInt);

    obj:=TObject(av[1].VDW);
    if obj is TPlanet then begin
    	with TPlanet(obj).FShopGoods[it] do begin
	    	Cnt:=Cnt+av[3].VInt;
        	av[0].VInt:=Cnt;
        end;
    end else if obj is TRuins then begin
    	with TRuins(obj).FShopGoods[it] do begin
	    	Cnt:=Cnt+av[3].VInt;
        	av[0].VInt:=Cnt;
        end;
    end else if obj is TShip then begin
    	with TShip(obj).FGoods[it] do begin
	    	Cnt:=Cnt+av[3].VInt;
        	av[0].VInt:=Cnt;
        end;
    end;

end;

procedure SF_GoodsCount(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
    it:TItemType;
begin
    if High(av)<>2 then raise Exception.Create('Error.Script GoodsCount');

    ship:=TShip(av[1].VDW);
    it:=TItemType(av[2].VInt);

    av[0].VInt:=ship.FGoods[it].Cnt;
end;

procedure SF_GoodsCost(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
    it:TItemType;
begin
    if High(av)<>2 then raise Exception.Create('Error.Script GoodsCost');

    ship:=TShip(av[1].VDW);
    it:=TItemType(av[2].VInt);

    av[0].VInt:=ship.FGoods[it].Cost;
end;

procedure SF_GoodsRuinsForBuy(av:array of TVarEC; code:TCodeEC);
var
    ruins:TRuins;
    it:tItemType;
begin
    if High(av)<>2 then raise Exception.Create('Error.Script GoodsRuinsForBuy');

    it:=TItemType(av[2].VInt);

    TRuins(av[1].VDW).MiniCostMaxSizeGoods([it]);
end;

procedure SF_ShipGoods(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
    it:TItemType;
    value:integer;
    costChange:integer;
begin
    if High(av)<3 then raise Exception.Create('Error.Script ShipGoods');

    ship:=TShip(av[1].VDW);
    it:=TItemType(av[2].VInt);
    value:=av[3].VInt;
    value:=max(value, -ship.FGoods[it].Cnt);

    //if value=0 then exit;

    if High(av)>3 then costChange:=av[4].VInt
    else if value>0 then costChange:=value*mGoods[it].AverageCost
    else costChange:=round(ship.FGoods[it].Cost*value/ship.FGoods[it].Cnt);

    ship.FGoods[it].Cnt:=ship.FGoods[it].Cnt+value;
    ship.FGoods[it].Cost:=ship.FGoods[it].Cost+costChange;
end;

procedure SF_ShipGoodsIllegalOnPlanet(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
  planet:TPlanet;
  prod:TItemType;
begin
  if High(av)<3 then raise Exception.Create('Error.Script ShipGoodsIllegalOnPlanet');

  ship:=TShip(av[1].VDW);
  prod:=TItemType(av[2].VInt);
  planet:=TPlanet(av[3].VDW);

  av[0].VInt:=0;

  if not (prod in Goods) then exit;
  if (planet.FOwner = PirateClan) then exit;

  if not mGoodsPermit[prod, planet.FRace, planet.FGoverment] then
  begin
    av[0].VInt := 1;
    Exit;
  end;

  if (prod in IllMolizonGoods) and ship.IllStimCur(IllMolizon) then
  begin
    av[0].VInt := 1;
    Exit;
  end;
end;

procedure SF_GoodsDrop(av:array of TVarEC; code:TCodeEC);
var
    it:tItemType;
    ship:TShip;
    tg:integer;
    item:TItem;
    sitem:TScriptItem;
    goods:TGoods;
    angle:single;
begin
    if High(av)<3 then raise Exception.Create('Error.Script GoodsDrop');

    ship:=TShip(av[1].VDW);
    it:=TItemType(av[2].VInt);

    tg:=min(ship.FGoods[it].Cnt,av[3].VInt);
    if tg<1 then begin av[0].VInt:=0; Exit; end;

    if ship<>Player then begin
        ship.DropGoods(it,tg);
        item:=PDropItem(ship.FCurStar.FItemsDrop.Items[ship.FCurStar.FItemsDrop.Count-1]).FItem as TItem;
    end else begin
        GR_SC.Play('Sound.Drop');
        dec(ship.FGoods[it].Cnt,tg);
        with Player.FCurStar do begin
            goods:=TGoods.Create;
            goods.Init(it,tg);
            FItems.Add(goods);

            angle:=Rnd(0,360,Player.FCurStar.FRnd*Galaxy.FTurn*ord(it))*pi/180;
            goods.FPos.x:=Player.FPos.x+sin(angle)*100;
            goods.FPos.y:=Player.FPos.y-cos(angle)*100;
            goods.GraphItem.Pos:=goods.FPos;

            item:=goods;
        end;
    end;

    if High(av)>=4 then begin
        sitem:=TScriptItem(av[4].VDW);

        if sitem.FItem<>nil then sitem.FItem.FScriptItem:=nil;

        sitem.FItem:=item;
        item.FScriptItem:=sitem;
    end;

    av[0].VInt:=1;
end;

procedure SF_UselessItemCreate(av:array of TVarEC; code:TCodeEC);
var
	item:TItem;
    sitem:TScriptItem;
    splace:TScriptPlace;
    a:single;
begin
    if High(av)<3 then raise Exception.Create('Error.Script UselessItemCreate');

	item:=TUselessItem.Create;
    (item as TUselessItem).Init(av[1].VStr,TDominatorSeries(rnd(ord(t_Blazer),ord(t_Terron))));

	sitem:=TScriptItem(av[2].VDW);

	if sitem.FItem<>nil then sitem.FItem.FScriptItem:=nil;

	sitem.FItem:=item;
    item.FScriptItem:=sitem;

	splace:=TScriptPlace(av[3].VDW);
	if (splace.FType<>0) and (splace.FType<>1) and (splace.FType<>3) and (splace.FType<>5) then EError('Error.Script UselessItemCreate place');

    splace.FStar.FItems.Add(item);
    item.FPos:=splace.GetCenter;
    a:=Angle360ToRad(Rnd(0,359,item.FId*Cardinal(splace.FStar.FRnd)));
    item.FPos.x:=item.FPos.x+splace.FRadius*sin(a);
    item.FPos.y:=item.FPos.y-splace.FRadius*cos(a);
end;

procedure SF_GoodsSellPrice(av:array of TVarEC; code:TCodeEC);
var
  obj:TObject;
  it:tItemType;
begin
    if High(av)<2 then raise Exception.Create('Error.Script GoodsSellPrice');

    obj:=TObject(av[1].VDW);
    it:=TItemType(av[2].VInt);

    if obj is TRuins then av[0].VInt:=TRuins(obj).FShopGoods[it].CostBuy
    else av[0].VInt:=TPlanet(obj).FShopGoods[it].CostBuy;

    if high(av)>2 then
    begin
      if obj is TRuins then TRuins(obj).FShopGoods[it].CostBuy:=av[3].VInt
      else TPlanet(obj).FShopGoods[it].CostBuy:=av[3].VInt;
    end;

end;

procedure SF_GoodsBuyPrice(av:array of TVarEC; code:TCodeEC);
var
  obj:TObject;
  it:tItemType;
begin
    if High(av)<2 then raise Exception.Create('Error.Script GoodsSellPrice');

    obj:=TObject(av[1].VDW);
    it:=TItemType(av[2].VInt);

    if obj is TRuins then av[0].VInt:=TRuins(obj).FShopGoods[it].CostSale
    else av[0].VInt:=TPlanet(obj).FShopGoods[it].CostSale;

    if high(av)>2 then
    begin
      if obj is TRuins then TRuins(obj).FShopGoods[it].CostSale:=av[3].VInt
      else TPlanet(obj).FShopGoods[it].CostSale:=av[3].VInt;
    end;

end;

procedure SF_CountTurn(av:array of TVarEC; code:TCodeEC);
var
    ship,ship2:TShip;
    cntt:integer;
    tobj:TObject;
    planet:TPlanet;
    splace:TScriptPlace;
    landing:boolean;
    tpos:TDxy;
    star:TStar;
begin
    if High(av)<>2 then raise Exception.Create('Error.Script CountTurn');

    cntt:=0;

    ship:=TShip(av[1].VDW);
    tobj:=TObject(av[2].VDW);
    if tobj is TScriptPlace then begin
        splace:=tobj as TScriptPlace;
        if (splace.FType=1) or (splace.FType=2) then begin
            planet:=splace.FObj as TPlanet;
            tpos:=planet.CartesianPos;
        end else begin
            planet:=nil;
            tpos:=splace.GetCenter;
        end;
        landing:=splace.FType=2;
        star:=splace.FStar;
    end else if tobj is TPlanet then begin
        planet:=tobj as TPlanet;
        landing:=false;
        tpos:=planet.CartesianPos;
        star:=planet.FStar;
	end else if tobj is TShip then begin
		landing:=false;
		planet:=nil;

    	ship2:=tobj as TShip;
        while ship2.FCurShip<>nil do ship2:=ship2.FCurShip;

        if ship2.FCurPlanet<>nil then begin
        	planet:=ship2.FCurPlanet;
            landing:=true;
	        tpos:=planet.CartesianPos;
    	    star:=planet.FStar;
        end else begin
    	    tpos:=ship2.FPos;
        	star:=ship2.FCurStar;

            if ship2.InHyperSpace then begin
	            tpos:=ship2.CalcAfterJumpPoint(ship2.FPrevStar);
            end;
        end;
    end else raise Exception.Create('Error.Script CountTurn 1');

    if (ship.FCurPlanet=planet) and landing then begin av[0].VInt:=0; exit; end;
    if (ship.FCurPlanet<>nil) then inc(cntt);
    if landing then inc(cntt);
    if (ship.FCurPlanet<>nil) and (ship.FCurPlanet=planet) then begin av[0].VInt:=cntt; exit; end;
    if star=ship.FCurStar then begin
        if ship.FCurPlanet=nil then cntt:=cntt+Ceil(Dist(tpos,ship.FPos)/max(1,Ship.FSpeed))
        else cntt:=cntt+Ceil(Dist(tpos,ship.FCurPlanet.CartesianPos)/max(1,Ship.FSpeed));
    end else begin
        if ship.FCurPlanet=nil then cntt:=cntt+Ceil(Dist(ship.CalcJumpPoint(star),ship.FPos)/max(1,ship.FSpeed))
        else cntt:=cntt+Ceil(Dist(ship.CalcJumpPoint(star),ship.FCurPlanet.CartesianPos)/max(1,ship.FSpeed));
        cntt:=cntt+ship.CalcTurnBetween(ship.FCurStar,star);

        cntt:=cntt+Ceil(Dist(tpos,ship.CalcAfterJumpPoint(star))/max(1,Ship.FSpeed));
    end;

    av[0].VInt:=cntt;
end;

procedure SF_ShipSetBad(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>2 then raise Exception.Create('Error.Script ShipSetBad');

    if av[1].VDW=0 then Exit;

    TShip(av[1].VDW).FShipBad:=Pointer(av[2].VDW);
end;

procedure SF_GroupSetBad(av:array of TVarEC; code:TCodeEC);
var
    no,i,cnt:integer;
    sship:TScriptShip;
begin
    if High(av)<>2 then raise Exception.Create('Error.Script GroupSetBad');

    no:=av[1].VInt;

    cnt:=GScriptCur.FShips.Count;
    for i:=0 to cnt-1 do begin
        sship:=GScriptCur.FShips.Items[i];
        if sship.FGroup=no then begin
            sship.FShip.FShipBad:=Pointer(av[2].VDW);
        end;
    end;
end;

procedure SF_ShipSetPartner(av:array of TVarEC; code:TCodeEC);
var ship,ship2:TShip;
begin
    if High(av)<>3 then raise Exception.Create('Error.Script ShipSetPartner');

    ship:=TShip(av[1].VDW);
    ship2:=TShip(av[2].VDW);

    if (ship is TPirate) and (ship.FShipPartner<>ship2) then
    begin
      if ship.FShipPartner = Player then Player.FPirates.Remove(ship);
      if ship2 = Player then Player.FPirates.Add(ship);
    end;

    ship.FShipPartner:=ship2;
    ship.FShipPartnerDay:=av[3].VInt;
end;

procedure SF_ShipJoin(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
    sship:TScriptShip;
    tcurship:Cardinal;
    v:TVarEC;
    es,stateNo,i:integer;
begin
    if High(av)<2 then raise Exception.Create('Error.Script ShipJoin');
    ship:=TShip(av[2].VDW);

    if ship=nil then exit;

    if (ship<>Player()) and (ship.FScriptShip<>nil) then
    begin
      if TScriptShip(ship.FScriptShip).FScript<>GScriptCur then
        SFT('Warning.Script ShipJoin ('+GScriptCur.FCD+'): ship '+ship.FullName+' was already in another script ('+TScriptShip(ship.FScriptShip).FScript.FCD+')');
      TScriptShip(ship.FScriptShip).FScript.DelShip(ship);
      ship.FScriptShip:=nil;
    end;


    tcurship:=Cardinal(GScriptCur.FCurShip);// .FCodeInit.LocalVar.GetVar('CurShip').VDW;
    v:=GScriptCur.FCodeInit.LocalVar.GetVar('EndState');
    es:=v.VInt;

    GScriptCur.AddShip(av[1].VInt,ship);
    sship:=SctiptGetSS(ship,GScriptCur);

    if (High(av)>=3) and (av[3].VType=vtStr) then
    begin
      stateNo:=-1;
      if av[3].VStr='' then stateNo:=TScriptGroup(GScriptCur.FGroup.Items[sship.FGroup]).FState
      else for i:=0 to GScriptCur.FState.Count-1 do
        if TScriptState(GScriptCur.FState[i]).FName=av[3].VStr then
        begin
          stateNo:=i;
          break;
        end;
      if stateNo<0 then  raise Exception.Create('Error.Script ShipJoin cant find state '+av[3].VStr);
    end
    else if High(av)>=3 then stateNo:=-1
    else stateNo:=TScriptGroup(GScriptCur.FGroup.Items[sship.FGroup]).FState;
    //if (High(av)<3) or (av[3].VType<>vtStr) then stateNo:=TScriptGroup(sship.FScript.FGroup.Items[sship.FGroup]).FState;

    if High(av)>=4 then sship.FData[0]:=av[4].VDW;
    if High(av)>=5 then sship.FData[1]:=av[5].VDW;
    if High(av)>=6 then sship.FData[2]:=av[6].VDW;
    if High(av)>=7 then sship.FData[3]:=av[7].VDW;

    if stateNo>=0 then GScriptCur.ChangeState(sship,stateNo);

    {if High(av)=3 then begin

    end else begin
        GScriptCur.ChangeState(sship,TScriptGroup(sship.FScript.FGroup.Items[sship.FGroup]).FState);
    end;}

    GScriptCur.FCodeInit.LocalVar.GetVar('CurShip').VDW:=Cardinal(tcurship);
    GScriptCur.FCurShip:=TShip(tcurship);
    v.VInt:=es;
end;

procedure SF_ShipOut(av:array of TVarEC; code:TCodeEC);
var
    ship:TShip;
begin
    if High(av)<1 then ship:=GScriptCur.FCurShip
    else ship:=TShip(av[1].VDW);

    if ship=nil then Exit;

    if ship=Player then GScriptCur.DelShip(ship)
    else if ship.FScriptShip<>nil then TScriptShip(ship.FScriptShip).FScript.DelShip(ship);
end;

procedure SF_AllShipOut(av:array of TVarEC; code:TCodeEC);
begin
    GScriptCur.DelAllShip;
end;

procedure SF_ShipInScript(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<1 then raise Exception.Create('Error.Script ShipInScript');

    if TShip(av[1].VDW).InScript or
      (((High(av)<=1) or (av[2].VInt<>0)) and (TShip(av[1].VDW).FScriptOrderAbsolute>0)) then av[0].VInt:=1
    else av[0].VInt:=0;
end;

procedure SF_ShipInGameEvent(av:array of TVarEC; code:TCodeEC);
var ship:TShip;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipInGameEvent');
    ship:=TShip(av[1].VDW);
    av[0].VInt:=0;

    if (ship is TWarrior) and ((ship as TWarrior).FGroup <> nil) then av[0].VInt:=1;
    if (ship is TRuins) and ((ship as TRuins).FFlyToStar <> nil) then av[0].VInt:=1;
end;

procedure SF_ShipInCurScript(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipInCurScript');

    if TShip(av[1].VDW).InScript and (SctiptGetSS(TShip(av[1].VDW),GScriptCur).FScript=GScriptCur) then av[0].VInt:=1
    else av[0].VInt:=0;
end;

procedure SF_ShipInNormalSpace(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipInNormalSpace');

    if (av[1].VDW<>0) and TShip(av[1].VDW).InNormalSpace then av[0].VInt:=1
    else av[0].VInt:=0;
end;

procedure SF_ShipInHole(av:array of TVarEC; code:TCodeEC);
var
	ship:TShip;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipInHole');

    ship:=TShip(av[1].VDW);
    if ship.InHyperSpace and (ship.FOrder=ORDER_JUMP_HOLE) then av[0].VInt:=1
    else av[0].VInt:=0;
end;

procedure SF_ShipIsTakeoff(av:array of TVarEC; code:TCodeEC);
var
	ship:TShip;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipIsTakeoff');

    ship:=TShip(av[1].VDW);
    if ship.FOrder=ORDER_TAKE_OFF then av[0].VInt:=1
    else av[0].VInt:=0;
end;

procedure SF_ShipCntWeapon(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipWeaponCount');

    av[0].VInt:=TShip(av[1].VDW).FWeaponCnt;
end;

procedure SF_ShipWeapon(av:array of TVarEC; code:TCodeEC);
var ship:TShip;
    no:integer;
begin
    if High(av)<>2 then raise Exception.Create('Error.Script ShipWeapon');
    ship:=TShip(av[1].VDW);
    no:=av[2].VInt;
    if (no<=0) or (no>ship.FWeaponCnt) then av[0].VDW:=0
    else av[0].VDW:=cardinal(ship.FWeapon[no]);
end;

procedure SF_ShipEqInSlot(av:array of TVarEC; code:TCodeEC);
var ship:TShip;
    it:TItemType;
    no:integer;
begin
    if High(av)<2 then raise Exception.Create('Error.Script ShipEqInSlot');
    ship:=TShip(av[1].VDW);
    it:=TItemType(av[2].VInt);//t_DefGenerator, t_Weapon1, t_Artefact etc
    if it in Equipments then
    begin
      av[0].VDW:=cardinal(ship.FEquip[it]);
      exit;
    end;
    if High(av)<3 then no:=0 else no:=av[3].VInt-1;//1..5 for weapons, 1..4 for arts
    ship.SlotCorrect;
    av[0].VDW:=cardinal(ship.SlotGetEquipment(it,no));
end;


procedure SF_ArtefactTypeInUse(av:array of TVarEC; code:TCodeEC);
var ship:TShip;
    art:TArtefact;
    it:TItemType;
    tstr:WideString;
    i,cnt:integer;
begin
    if High(av)<2 then raise Exception.Create('Error.Script ArtefactTypeInUse');
    ship:=TShip(av[1].VDW);

    art:=nil;
    if (av[2].VType = vtDW) and (av[2].VDW > 65535) then art:=TArtefact(av[2].VDW);

    tstr:='';
    if (art<>nil) and (art.EffectiveItemType in CustomArtefacts) then tstr:=art.FSysName
    else if av[2].VType = vtStr then tstr:=av[2].VStr;

    if tstr<>'' then
    begin
      cnt:=0;
      for i:=0 to ship.FArtefacts.Count-1 do
      begin
        art:=ship.FArtefacts[i];
        if not (art.FItemType in CustomArtefacts) then continue;
        if art.FSysName<>tstr then continue;
        if art.FBroken then continue;
        if art.FExplotable then inc(cnt);
      end;
      av[0].VInt:=cnt;
      exit;
    end;

    if art<>nil then it:=TArtefact(av[2].VDW).EffectiveItemType
    else it:=TItemType(av[2].VInt);

    av[0].VInt:=ship.ArtefactExplotable(it);
end;

procedure SF_ArtefactTypeBoosted(av:array of TVarEC; code:TCodeEC);
var ship:TShip;
    it:TItemType;
begin
    if High(av)<2 then raise Exception.Create('Error.Script ArtefactTypeBoosted');
    ship:=TShip(av[1].VDW);

    if (av[2].VType = vtDW) and (av[2].VDW > 255) then it:=TArtefact(av[2].VDW).EffectiveItemType
    else it:=TItemType(av[2].VInt);

    av[0].VInt:=ord(ship.ArtefactExBoost(it));
end;

procedure SF_ShipGroup(av:array of TVarEC; code:TCodeEC);
var sship:TScriptShip;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipGroup');

    sship:=SctiptGetSS(TShip(av[1].VDW),GScriptCur);

    if sship<>nil then av[0].VInt:=sship.FGroup
    else av[0].VInt:=-1;
end;

procedure SF_ShipSpeed(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipSpeed');
    av[0].VInt:=TShip(av[1].VDW).FSpeed;
end;

procedure SF_EnginePower(av:array of TVarEC; code:TCodeEC);
var obj:TObject;
    eng:TEngine;
begin
    if High(av)<1 then raise Exception.Create('Error.Script EnginePower');
    obj:=TObject(Cardinal(av[1].VDW));
    eng:=nil;
    if (obj is TEngine) then eng:=TEngine(obj)
    else if (obj is TScriptItem) and ((obj as TScriptItem).FItem <> nil) and ((obj as TScriptItem).FItem is TEngine) then eng:=TEngine((obj as TScriptItem).FItem)
    else if obj is TShip then eng:=TShip(obj).FEngine;
    if eng<>nil then
    begin
      av[0].VInt:=eng.FPower;
      if High(av)>1 then eng.FPower:=av[2].VInt;
    end else av[0].VInt:=0;
end;

procedure SF_ShipJump(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipJump');
    av[0].VInt:=TShip(av[1].VDW).GiperJumpInTheory;
end;

procedure SF_ShipArmor(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipArmor');
    av[0].VInt:=TShip(av[1].VDW).HullDef;
end;

procedure SF_ShipProtectability(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipProtectability');
    av[0].VInt:=Round(100*(1-TShip(av[1].VDW).Protectability));
end;

procedure SF_ShipDroidRepair(av:array of TVarEC; code:TCodeEC);
var ship:TShip;
    repair:integer;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipDroidRepair');
    av[0].VInt:=0;
    ship:=TShip(av[1].VDW);
    if not ship.AbleToUse(ship.RepairRobot) then exit;
    av[0].VInt:=ship.CalculateDroidRepair(ship.RepairRobot);
end;

procedure SF_ShipRadarRange(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipRadarRange');
    av[0].VInt:=TShip(av[1].VDW).RadarRange;
end;

procedure SF_ShipScanerPower(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipScanerPower');
    av[0].VInt:=TShip(av[1].VDW).ScanerPower;
end;

procedure SF_ShipHookPower(av:array of TVarEC; code:TCodeEC);
var ship:TShip;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipHookPower');
    av[0].VInt:=0;
    ship:=TShip(av[1].VDW);
    if not ship.AbleToUse(ship.CargoHook) then exit;

    av[0].VInt:=ship.CalculateCargoHookPower(ship.CargoHook);
end;

procedure SF_ShipHookRange(av:array of TVarEC; code:TCodeEC);
var ship:TShip;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ShipHookRange');
    av[0].VInt:=0;
    ship:=TShip(av[1].VDW);
    if not ship.AbleToUse(ship.CargoHook) then exit;

    av[0].VInt:=ship.CargoHookRadius;
end;

procedure SF_ShipAverageDamage(av:array of TVarEC; code:TCodeEC);
var ship:TShip;
    i, minDamage, maxDamage: integer;
    weapon: TWeapon;
begin
    if High(av)<1 then raise Exception.Create('Error.Script ShipAverageDamage');
    ship:=TShip(av[1].VDW);
    minDamage:=0; maxDamage:=0;

    for i:=1 to ship.FWeaponCnt do
    begin
      weapon:=ship.FWeapon[i];
      if not ship.AbleToUse(weapon) then continue;

      if weapon.WeaponInfo.ShotType in [shtRocket,shtMissile] then
      begin
        minDamage := minDamage + ship.WeaponMinDamage(weapon) * weapon.AttackCount * weapon.ShotCount;
        maxDamage := maxDamage + ship.WeaponMaxDamage(weapon) * weapon.AttackCount * weapon.ShotCount;
      end else begin
        minDamage := minDamage + ship.WeaponMinDamage(weapon) * weapon.AttackCount;
        maxDamage := maxDamage + ship.WeaponMaxDamage(weapon) * weapon.AttackCount;
      end;
    end;
    if High(av)>1 then
    begin
      if av[2].VInt=0 then av[0].VInt:=minDamage
      else if av[2].VInt=1 then av[0].VInt:=maxDamage
      else av[0].VInt:=Round(0.5*(minDamage+maxDamage));
    end else av[0].VInt:=Round(0.5*(minDamage+maxDamage));
end;

procedure SF_ShipHealthFactor(av:array of TVarEC; code:TCodeEC);
var ship:TShip;
    i,dur,dur2:integer;
begin
  if High(av)<2 then raise Exception.Create('Error.Script ShipHealthFactor');
  ship:=TShip(av[1].VDW);
  i:=av[2].VInt;
  dur:=0;

  if ship = nil then
  begin
    if i=0 then av[0].VInt:=mEIllness[1].Time
    else av[0].VInt:=mIllness[i].Time;
    exit;
  end;

  if i=0 then
  begin
    if ship.IllRadiation then dur:=ship.FmEInfections[EIllRadiation].InfectionEndDay-Galaxy.FTurn;
    if High(av)>2 then
    begin
      dur2:=av[3].VInt;
      if dur2 = -1 then dur2:=mEIllness[EIllRadiation].Time;
      if (dur>0) and (dur2=0) then
      begin
        ship.FmEInfections[EIllRadiation].Infection:=0;
        ship.FmEInfections[EIllRadiation].InfectionEndDay:=0;
      end;
      if (dur=0) and (dur2>0) then
      begin
        ship.FmEInfections[EIllRadiation].Infection:=0.5;
        ship.FmEInfections[EIllRadiation].InfectionEndDay:=Galaxy.FTurn+dur2;
      end;
      if (dur>0) and (dur2>0) then ship.FmEInfections[EIllRadiation].InfectionEndDay:=Galaxy.FTurn+dur2;
    end;
  end else if (i>0) and (i<=IllStimCnt) then
  begin
    if ship.IllStimCur(i) then dur:=ship.FmInfections[i].InfectionEndDay-Galaxy.FTurn;
    if High(av)>2 then
    begin
      dur2:=av[3].VInt;
      if dur2 = -1 then dur2:=mIllness[i].Time;
      if (dur>0) and (dur2=0) then
      begin
        ship.FmInfections[i].Infection:=0;
        ship.FmInfections[i].InfectionEndDay:=0;
      end;
      if (dur=0) and (dur2>0) then
      begin
        ship.FmInfections[i].Infection:=100;
        ship.FmInfections[i].InfectionEndDay:=Galaxy.FTurn+dur2;
      end;
      if (dur>0) and (dur2>0) then ship.FmInfections[i].InfectionEndDay:=Galaxy.FTurn+dur2;
    end;
  end;
  av[0].VInt:=dur;
end;

procedure SF_ShipHealthFactorStatus(av:array of TVarEC; code:TCodeEC);
var ship:TShip;
    i,dur,dur2:integer;
begin
  if High(av)<2 then raise Exception.Create('Error.Script ShipHealthFactorStatus');
  ship:=TShip(av[1].VDW);
  i:=av[2].VInt;

  if i=0 then
  begin
    av[0].VInt:=round(ship.FmEInfections[EIllRadiation].Infection);
    if High(av)>2 then ship.FmEInfections[EIllRadiation].Infection:=av[3].VInt;
  end
  else if (i>0) and (i<=IllStimCnt) then
  begin
    av[0].VInt:=round(ship.FmInfections[i].Infection);
    if High(av)>2 then ship.FmInfections[i].Infection:=av[3].VInt;
  end
  else av[0].VInt:=0;
  //0 - no illness
  //1-99 - hidden illness
  //100 - active illness
end;

procedure SF_PlayerImmunity(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=Player.FImmunity;
  if High(av)>=1 then Player.FImmunity:=av[1].VInt;
end;

procedure SF_ShipStatusEffect(av:array of TVarEC; code:TCodeEC);
var ship:TShip;
    effType:TStatusEffectType;
    no:integer;
    change:single;
    source:TShip;
begin
  if High(av)<2 then raise Exception.Create('Error.Script ShipStatusEffect');

  ship:=TShip(av[1].VDW);
  effType:=TStatusEffectType(av[2].VInt);//steShock, steAcid, steMagnetic, steWeaponBlock, steDroidBlock, steBWBuff, steBWRepairDebuff

  no:=ship.StatusEffectFind(effType);
  if no<0 then av[0].VFloat:=0
  else av[0].VFloat:=PStatusEffects(ship.FStatusEffects[no]).EffectStrength;

  if High(av)>2 then //+-change, not a new value
  begin
    change:=av[3].VFloat;
    if High(av)>3 then source:=TShip(av[4].VDW) else source:=nil;
    if change>0 then ship.AddStatusEffectStrength(effType,change,source)
    else if change<0 then ship.ReduceStatusEffectStrength(effType,-change);
  end;
end;

procedure SF_GroupIs(av:array of TVarEC; code:TCodeEC);
var
    i,cnt,nogroup:integer;
begin
    if High(av)<2 then raise Exception.Create('Error.Script GroupIs');

    nogroup:=SctiptGetSS(TShip(av[1].VDW),GScriptCur).FGroup;
    cnt:=High(av)+1-2;
    for i:=0 to cnt-1 do begin
        if nogroup=av[2+i].VInt then begin
            av[0].VInt:=1;
            Exit;
        end;
    end;
    av[0].VInt:=0;
end;

procedure SF_StateIs(av:array of TVarEC; code:TCodeEC);
var
    i,cnt:integer;
    sstate:TScriptState;
    sship:TScriptShip;
begin
    if High(av)<2 then raise Exception.Create('Error.Script StateIs');

    sship:=SctiptGetSS(TShip(av[1].VDW),GScriptCur);
    if sship=nil then begin av[0].VInt:=0; exit; End;

    sstate:=sship.FState;
    if sstate=nil then begin av[0].VInt:=0; exit; End;

    cnt:=High(av)+1-2;
    for i:=0 to cnt-1 do begin
        if sstate.FName=av[2+i].VStr then begin
            av[0].VInt:=1;
            Exit;
        end;
    end;
    av[0].VInt:=0;
end;


procedure SF_Dist(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  pos1,pos2: TPos;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script Dist');
  av[0].VInt:=0;

  obj:=TObject(av[1].VDW);
  if(obj <> nil) then
  begin
    if(obj is TShip) then pos1:=(obj as TShip).FPos
    else if(obj is TItem) then pos1:=(obj as TItem).FPos
    else if(obj is TScriptItem) then
    begin
      if((obj as TScriptItem).FItem <> nil) then pos1:=(obj as TScriptItem).FItem.FPos
      else raise Exception.Create('Error.Script Dist 1');
    end else if(obj is TScriptPlace) then pos1:=(obj as TScriptPlace).GetCenter
    else if(obj is TPlanet) then pos1:=(obj as TPlanet).CartesianPos
    else if(obj is TStar) then pos1:=(obj as TStar).FPos
    else if(obj is TAsteroid) then pos1:=(obj as TAsteroid).FPos
    else if(obj is TMissile) then pos1:=(obj as TMissile).FPos
    else raise Exception.Create('Error.Script Dist 2');

    obj:=TObject(av[2].VDW);
    if(obj <> nil) then
    begin
      if(obj is TShip) then pos2:=(obj as TShip).FPos
      else if(obj is TItem) then pos2:=(obj as TItem).FPos
      else if(obj is TScriptItem) then
      begin
        if((obj as TScriptItem).FItem <> nil) then pos2:=(obj as TScriptItem).FItem.FPos
        else raise Exception.Create('Error.Script Dist 3');
      end else if(obj is TScriptPlace) then pos2:=(obj as TScriptPlace).GetCenter
      else if(obj is TPlanet) then pos2:=(obj as TPlanet).CartesianPos
      else if(obj is TStar) then pos2:=(obj as TStar).FPos
      else if(obj is TAsteroid) then pos2:=(obj as TAsteroid).FPos
      else if(obj is TMissile) then pos2:=(obj as TMissile).FPos
      else raise Exception.Create('Error.Script Dist 4');

      av[0].VInt:=Round(Dist(pos1,pos2));
    end;
  end;
end;

procedure SF_Angle(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  pos1,pos2: TPos;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script Angle');
  av[0].VInt:=0;

  obj:=TObject(av[1].VDW);
  if(obj <> nil) then
  begin
    if(obj is TShip) then pos1:=(obj as TShip).FPos
    else if(obj is TItem) then pos1:=(obj as TItem).FPos
    else if(obj is TScriptItem) then
    begin
      if((obj as TScriptItem).FItem <> nil) then pos1:=(obj as TScriptItem).FItem.FPos
      else raise Exception.Create('Error.Script Dist 1');
    end else if(obj is TScriptPlace) then pos1:=(obj as TScriptPlace).GetCenter
    else if(obj is TPlanet) then pos1:=(obj as TPlanet).CartesianPos
    else if(obj is TStar) then pos1:=(obj as TStar).FPos
    else if(obj is TAsteroid) then pos1:=(obj as TAsteroid).FPos
    else if(obj is TMissile) then pos1:=(obj as TMissile).FPos
    else raise Exception.Create('Error.Script Dist 2');

    obj:=TObject(av[2].VDW);
    if(obj <> nil) then
    begin
      if(obj is TShip) then pos2:=(obj as TShip).FPos
      else if(obj is TItem) then pos2:=(obj as TItem).FPos
      else if(obj is TScriptItem) then
      begin
        if((obj as TScriptItem).FItem <> nil) then pos2:=(obj as TScriptItem).FItem.FPos
        else raise Exception.Create('Error.Script Dist 3');
      end else if(obj is TScriptPlace) then pos2:=(obj as TScriptPlace).GetCenter
      else if(obj is TPlanet) then pos2:=(obj as TPlanet).CartesianPos
      else if(obj is TStar) then pos2:=(obj as TStar).FPos
      else if(obj is TAsteroid) then pos2:=(obj as TAsteroid).FPos
      else if(obj is TMissile) then pos2:=(obj as TMissile).FPos
      else raise Exception.Create('Error.Script Dist 4');

      av[0].VInt:=Round(AngleCalc(pos2,pos1));
    end;
  end;
end;

procedure SF_Dist2Star(av:array of TVarEC; code:TCodeEC);
begin
  if High(av)<>2 then raise Exception.Create('Error.Script DistStar');
  av[0].VFloat:=Dist2(TStar(av[1].VDW).FPos,TStar(av[2].VDW).FPos);
end;


procedure SF_BuyPirate(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  ship: TShip;
  monPerc:integer;
  flag:boolean;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script BuyPirate');
  monPerc:=100;
  if (High(av) > 1) then monPerc:=av[2].VInt;
  planet:=TPlanet(av[1].VDW);
  if(planet <> nil) then begin
    flag:=planet.FIsMainPiratePlanet; planet.FIsMainPiratePlanet:=false;
    ship:=TShip(planet.BuyPirate(monPerc));
    planet.FIsMainPiratePlanet:=flag;
    av[0].VDW:=Cardinal(ship);
  end;
end;


procedure SF_BuyTransport(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  ship: TShip;
  shiptype: TSShipType;
  monPerc:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script BuyTransport');
  planet:=TPlanet(av[1].VDW);
  monPerc:=100;
  if (High(av) > 2) then monPerc:=av[3].VInt;

  if(planet <> nil) then
  begin
    if(High(av) > 1) then
    begin
      case (av[2].VInt) of
        0: shiptype:=ts_Transport;
        1: shiptype:=ts_Liner;
        2: shiptype:=ts_Diplomat;
        else shiptype:=ts_Ranger;
      end;
    end else shiptype:=ts_Ranger;
    ship:=TShip(planet.BuyTransport(shiptype,monPerc));
    av[0].VDW:=Cardinal(ship);
  end;
end;

procedure SF_Name(av:array of TVarEC; code:TCodeEC);
var
  obj:TObject;
begin
  if High(av)<>1 then raise Exception.Create('Error.Script Name');
  obj:=TObject(av[1].VDW);

  if obj is TStar then av[0].VStr:=TStar(obj).FName
  else if obj is TConstellation then av[0].VStr:=TConstellation(obj).Name
  else if obj is TPlanet then av[0].VStr:=TPlanet(obj).FName
  else if obj is TShip then av[0].VStr:=TShip(obj).FullName
  else if obj is TScriptItem then
  begin
    if TScriptItem(obj).FItem=nil then av[0].VStr:='NameError'
    else av[0].VStr:=TScriptItem(obj).FItem.Name;
  end else if obj is TItem then av[0].VStr:=TItem(obj).Name
  else av[0].VStr:='NameError';
end;

procedure SF_ShortName(av:array of TVarEC; code:TCodeEC);
var
    obj:TObject;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script Name');
	  obj:=TObject(av[1].VDW);

    if obj is TStar then av[0].VStr:=TStar(obj).FName
    else if obj is TPlanet then av[0].VStr:=TPlanet(obj).FName
    else if obj is TShip then av[0].VStr:=TShip(obj).Name
	  else if obj is TScriptItem then
    begin
    	if TScriptItem(obj).FItem=nil then av[0].VStr:='NameError'
    	else av[0].VStr:=TScriptItem(obj).FItem.ShortName;
    end else if obj is TItem then av[0].VStr:=TItem(obj).ShortName
    else av[0].VStr:='NameError';
end;

procedure SF_FirstGiveMoney(av:array of TVarEC; code:TCodeEC);
begin
	av[0].VInt:=Round(300*mDifLevel[Galaxy.FDifLevels[dTrade]].kMoney);
end;

//procedure SF_ScenarioState(av:array of TVarEC; code:TCodeEC);
//begin
//	av[0].VInt:=0;
//obsolete
//end;

//procedure SF_HaveCommunicator(av:array of TVarEC; code:TCodeEC);
//begin
//	av[0].VInt:=0;
//obsolete
//end;

procedure SF_HaveProgramm(av:array of TVarEC; code:TCodeEC);
begin
  if High(av)<>1 then raise Exception.Create('Error.Script HaveProgramm');
	av[0].VInt:=integer(Player.HaveProgramm(TProgramms(av[1].VDW)));
end;

procedure SF_GetProgramm(av:array of TVarEC; code:TCodeEC);
begin
  if High(av)<1 then raise Exception.Create('Error.Script GetProgramm');
  av[0].VInt:=Player.FmProgramms[TProgramms(av[1].VDW)];
end;

procedure SF_SetProgramm(av:array of TVarEC; code:TCodeEC);
begin
  if High(av)<2 then raise Exception.Create('Error.Script SetProgramm');
  av[0].VInt:=integer(Player.HaveProgramm(TProgramms(av[1].VDW)));
  Player.FmProgramms[TProgramms(av[1].VDW)]:=av[2].VInt;
end;

procedure SF_DomikProgramm(av:array of TVarEC; code:TCodeEC);
var
  kling:TKling;
  prog:TProgramms;
  cnt:integer;
begin
  if High(av)<1 then raise Exception.Create('Error.Script DomikProgramm');
  kling:=TKling(av[1].VDW);
  av[0].VInt:=integer(kling.FRunProgrammName);
  if High(av)>1 then
  begin
    prog:=TProgramms(av[2].VDW);
    kling.FRunProgrammName := prog;

    case prog of
      progShipwreck:
      begin // Получив аварийный сигнал доминатор выбросит часть оборудования и оружия.
        if High(av)>2 then cnt:=av[3].VInt else cnt:=Rnd(1, 3, Galaxy.FTurn);
        kling.DropRndEquipment(cnt);
      end;
      progSelfDestruction:
      begin
        kling.FShipDestroy := True;
      end;
      progDisconnection:
      begin
        kling.OrderNone;
        kling.NotAttack;
      end;
    end;
  end;
end;

procedure SF_DomikProgrammDate(av:array of TVarEC; code:TCodeEC);
var
  kling:TKling;
  prog:TProgramms;
begin
  if High(av)<1 then raise Exception.Create('Error.Script DomikProgrammDate');
  kling:=TKling(av[1].VDW);
  av[0].VInt:=kling.FRunProgrammDate;
  if High(av)>1 then kling.FRunProgrammDate := av[2].VInt;
end;

procedure SF_HoleMamaCreate(av:array of TVarEC; code:TCodeEC);
var
	a,r:single;
  hole:THole;
	i:integer;
  lFilmObj:TEFilmObj;
begin
  hole:=THole.Create;
  hole.Init;
	hole.FGraphHole.State:=1;
  hole.FStar1:=Blazer.FCurStar;



  hole.FPos1.x:=Blazer.FPos.x-Player.FPos.x;
  hole.FPos1.y:=Blazer.FPos.y-Player.FPos.y;
  r:=1/sqrt(sqr(hole.FPos1.x)+sqr(hole.FPos1.y));
  hole.FPos2.x:=hole.FPos1.x*r;
  hole.FPos2.y:=hole.FPos1.y*r;

  hole.FPos1.x:=Blazer.FPos.x+hole.FPos2.x*200;
  hole.FPos1.y:=Blazer.FPos.y+hole.FPos2.y*200;
  r:=sqrt(sqr(hole.FPos1.x)+sqr(hole.FPos1.y));
  if r<Blazer.FCurStar.FSafeRadius then
  begin
    hole.FPos1.x:=Blazer.FPos.x-hole.FPos2.y*200;
    hole.FPos1.y:=Blazer.FPos.y+hole.FPos2.x*200;
    r:=sqrt(sqr(hole.FPos1.x)+sqr(hole.FPos1.y));
    if r<Blazer.FCurStar.FSafeRadius then
    begin
      hole.FPos1.x:=Blazer.FPos.x+hole.FPos2.y*200;
      hole.FPos1.y:=Blazer.FPos.y-hole.FPos2.x*200;
    end;
  end;

	hole.FStar2:=nil;
	a:=1e20;
	for i:=0 to Galaxy.FStars.Count-1 do
  begin
    r:=Dist2(Blazer.FCurStar.FPos,TStar(Galaxy.FStars.Items[i]).FPos);
    if (r>5) and (r<a) then
    begin
      a:=r;
      hole.FStar2:=Galaxy.FStars.Items[i];
    end;
  end;

  a:=Angle360ToRad(Rnd(0,359,Galaxy.FRndOut));
  r:=Rnd(1000,2000,Galaxy.FRndOut);
  hole.FPos2:=Dxy(sin(a)*r,-cos(a)*r);

  hole.FTurnCreate:=Galaxy.FTurn;
  hole.FType:=2;
  Galaxy.FHoles.Add(hole);

	if hole.FStar1.FFilmBuild or hole.FStar2.FFilmBuild then
  begin
		lFilmObj:=GFilm.ObjAdd(hole.FId,hole.FGraphHole,'','');
    GFilm.OrderMove(0,lFilmObj,hole.FPos1);
    GFilm.OrderHoleState(0,lFilmObj,1);
    GFilm.OrderGraphConnect(0,lFilmObj);
  end;
end;

procedure SF_HoleCreate(av:array of TVarEC; code:TCodeEC);
var
  hole:THole;
  a:single;
  splace:TScriptPlace;
  lFilmObj:TEFilmObj;
begin
  if High(av)<>2 then raise Exception.Create('Error.Script HoleCreate');

  hole:=THole.Create;
  hole.Init;
  hole.FGraphHole.State:=1;
  hole.FTurnCreate:=Galaxy.FTurn;
  hole.FType:=1;

  splace:=TScriptPlace(av[1].VDW);
  if (splace.FType<>0) and (splace.FType<>1) and (splace.FType<>3) and (splace.FType<>5) then EError('Error.Script HoleCreate place 1');

  hole.FStar1:=splace.FStar;

  a:=Angle360ToRad(Rnd(0,359,hole.FId*Cardinal(hole.FStar1.FRnd)));
  hole.FPos1:=splace.GetCenter;
  hole.FPos1.x:=hole.FPos1.x+splace.FRadius*sin(a);
  hole.FPos1.y:=hole.FPos1.y-splace.FRadius*cos(a);

  splace:=TScriptPlace(av[2].VDW);
  if (splace.FType<>0) and (splace.FType<>1) and (splace.FType<>3) and (splace.FType<>5) then EError('Error.Script HoleCreate place 1');

  hole.FStar2:=splace.FStar;

  a:=Angle360ToRad(Rnd(0,359,hole.FId*Cardinal(hole.FStar2.FRnd)));
  hole.FPos2:=splace.GetCenter;
  hole.FPos2.x:=hole.FPos2.x+splace.FRadius*sin(a);
  hole.FPos2.y:=hole.FPos2.y-splace.FRadius*cos(a);

  Galaxy.FHoles.Add(hole);

  if hole.FStar1.FFilmBuild or hole.FStar2.FFilmBuild then
  begin
		lFilmObj:=GFilm.ObjAdd(hole.FId,hole.FGraphHole,'','');
    GFilm.OrderMove(0,lFilmObj,hole.FPos1);
    GFilm.OrderHoleState(0,lFilmObj,1);
    GFilm.OrderGraphConnect(0,lFilmObj);
  end else if Player.InNormalSpace and ((Player.FCurStar=hole.FStar1) or (Player.FCurStar=hole.FStar2)) then GFormStarMap.FOpenHole := hole;

end;

procedure SF_TerronWeaponLock(av:array of TVarEC; code:TCodeEC);
begin
	Galaxy.FTerronWeaponLockTurn:=Galaxy.FTurn;
end;

procedure SF_TerronGrowLock(av:array of TVarEC; code:TCodeEC);
begin
	Galaxy.FTerronGrowLockTurn:=Galaxy.FTurn;
end;

procedure SF_TerronLandingLock(av:array of TVarEC; code:TCodeEC);
begin
	Galaxy.FTerronLandingLockTurn:=Galaxy.FTurn;
end;

procedure SF_TerronToStar(av:array of TVarEC; code:TCodeEC);
begin
	Galaxy.FTerronToStar:=Galaxy.FTurn;
end;

procedure SF_KellerLeave(av:array of TVarEC; code:TCodeEC);
begin
	Galaxy.FKellerLeave:=Galaxy.FTurn;
end;

procedure SF_KellerNewResearch(av:array of TVarEC; code:TCodeEC);
begin
	Galaxy.FKellerNewResearch:=av[1].VDW;
end;

procedure SF_KellerKill(av:array of TVarEC; code:TCodeEC);
begin
	GABKellerKill:=true;
end;

procedure SF_BlazerLanding(av:array of TVarEC; code:TCodeEC);
var i:integer;
    weapon:TWeapon;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script BlazerLanding');

    Galaxy.FBlazerLanding:=av[1].VDW;
    if Blazer<>nil then
    begin
      Blazer.CalcStanding;
      Blazer.FShipBad:=nil;
      for i := 1 to Blazer.FWeaponCnt do
      begin
        weapon := Blazer.FWeapon[i];
        if weapon<>nil then weapon.FTarget:=nil;
      end;
    end;
end;

procedure SF_BlazerSelfDestruction(av:array of TVarEC; code:TCodeEC);
begin
    Galaxy.FBlazerSelfDestruction:=Galaxy.FTurn;
end;

procedure SF_GalaxyShipId(av:array of TVarEC; code:TCodeEC);
begin
    av[0].VInt:=Galaxy.FIdShip;
end;

procedure SF_NearCivilPlanet(av:array of TVarEC; code:TCodeEC);
var
	i:integer;
    d,dmin:single;
	ship:TShip;
    planet:TPlanet;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script NearCivilPlanet');

    ship:=TShip(av[1].VDW);

    av[0].VDW:=0;

    dmin:=1e30;
    for i:=0 to ship.FCurStar.FPlanets.Count-1 do begin
    	planet:=TPlanet(ship.FCurStar.FPlanets.Items[i]);
        if planet.FOwner=None then continue;
    	d:=Dist2(ship.FPos,planet.CartesianPos);
        if d<dmin then begin
        	dmin:=d;
            av[0].VDW:=Cardinal(planet);
        end;
    end;

end;

procedure SF_SkipGreeting(av:array of TVarEC; code:TCodeEC);
begin
	GScriptCur.FSkipGreeting:=true;
end;

procedure SF_Sound(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script Sound');
	  GR_SC.Play(av[1].VStr);
end;

procedure SF_Tips(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script Tips');
    Tips(av[1].VInt);
end;

procedure SF_TipsState(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script TipsState');
    av[0].VInt:=ord(TipsState(av[1].VInt));
end;

procedure SF_CT(av:array of TVarEC; code:TCodeEC);
var
	tstr:WideString;
begin
    if High(av)<>1 then raise Exception.Create('Error.Script CT');

    tstr:=CTExt(av[1].VStr);
   	if FindSubString(tstr,'<')>=0 then begin
	    tstr:=StringReplaceEC(tstr,'<br>',ll);
	    if Player<>nil then begin
        	tstr:=StringReplaceEC(tstr,'<PlayerFull>',ColorStr(Player.FullName,txtStandart));
        end;
    end;
    av[0].VStr:=StringReplaceEC(tstr,ll+' ',ll);
end;

procedure SF_BlockExist(av:array of TVarEC; code:TCodeEC);
var
	tstr:WideString;
  i,cnt:integer;
  bpp: TBlockParEC;
begin
    if High(av)<1 then raise Exception.Create('Error.Script BlockExist');
    tstr:=av[1].VStr;
    cnt:=GetCountParEC(tstr,'.');

    if High(av)<2 then bpp:=GR_BPLang
    else begin
      if      av[2].VStr = 'Lang' then bpp:=GR_BPLang
      else if av[2].VStr = 'Main' then bpp:=GR_BPM
      else if av[2].VStr = 'Config' then bpp:=GR_User
      else raise Exception.Create('Error.Script BlockExist - unknown type '+av[2].VStr);
    end;

    av[0].VInt:=0;
    for i:=0 to cnt-1 do
    begin
      if bpp.Block_Count(GetStrParEC(tstr,i,'.')) = 0 then exit;
      bpp:=bpp.Block[GetStrParEC(tstr,i,'.')];
    end;
    av[0].VInt:=1;
end;

procedure SF_GetMainData(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script GetMainData');

    if GR_BPM.ParPath_Count(av[1].VStr)>0 then av[0].VStr:=GR_BPM.ParPath_Get(av[1].VStr) else av[0].VStr:='';
end;

procedure SF_GetGameOptions(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script GetGameOptions');
    if av[1].VStr = 'ResolutionX' then begin av[0].VInt:=GR_ScreenLenX; exit; end;
    if av[1].VStr = 'ResolutionY' then begin av[0].VInt:=GR_ScreenLenY; exit; end;

    try
      av[0].VStr:=GR_User.Par[av[1].VStr];
    except
      av[0].VStr:='';
    end;
end;

procedure SF_ResourceExist(av:array of TVarEC; code:TCodeEC);
begin
    if High(av)<>1 then raise Exception.Create('Error.Script ResourceExist');
    av[0].VInt:=ord(GR_Data.ExistsFile(av[1].VStr));
end;


procedure SF_CurrentMods(av:array of TVarEC; code:TCodeEC);
var
	tstr:WideString;
  i,cnt:integer;
  bpp: TBlockParEC;
begin
  if High(av)<1 then av[0].VInt:=GetCountParEC(GR_UsedMods,',')
  else av[0].VStr:=GetStrParEC(GR_UsedMods,av[1].VInt,',');
end;


procedure SF_RobotSupport(av:array of TVarEC; code:TCodeEC);
begin
    av[0].VInt:=integer((GIRobot<>nil) and (GIRobot.FSupport()=0));
end;



procedure SF_StarShips(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  no: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script StarShips');
  star:=TStar(av[1].VDW);
  if(star <> nil) then begin
    if(High(av) = 1) then begin
      av[0].VInt:=star.FShips.Count;
    end else begin
      no:=av[2].VInt;
      if(no >= 0) and (no < star.FShips.Count) then av[0].VDW:=Cardinal(star.FShips.Items[no]) else av[0].VDW:=0;
    end;
  end;
end;


procedure SF_StarPlanets(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  no: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script StarPlanets');
  star:=TStar(av[1].VDW);
  if(star <> nil) then
  begin
    if(High(av) = 1) then
    begin
      av[0].VInt:=star.FPlanets.Count;
    end else begin
      no:=av[2].VInt;
      if(no >= 0) and (no < star.FPlanets.Count) then av[0].VDW:=Cardinal(star.FPlanets.Items[no]) else av[0].VDW:=0;
    end;
  end;
end;

procedure SF_StarMissiles(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  no: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script StarMissiles');
  star:=TStar(av[1].VDW);
  if(star <> nil) then
  begin
    if(High(av) = 1) then
    begin
      av[0].VInt:=star.FMissile.Count;
    end else begin
      no:=av[2].VInt;
      if(no >= 0) and (no < star.FMissile.Count) then av[0].VDW:=Cardinal(star.FMissile.Items[no]) else av[0].VDW:=0;
    end;
  end;
end;

procedure SF_StarAsteroids(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  no: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script StarAsteroids');
  star:=TStar(av[1].VDW);
  if(star <> nil) then
  begin
    if(High(av) = 1) then
    begin
      av[0].VInt:=star.FAsteroids.Count;
    end else begin
      no:=av[2].VInt;
      if(no >= 0) and (no < star.FAsteroids.Count) then av[0].VDW:=Cardinal(star.FAsteroids.Items[no]) else av[0].VDW:=0;
    end;
  end;
end;


procedure SF_GroupShip(av:array of TVarEC; code:TCodeEC);
var
  sship: TScriptShip;
  i,cnt,no,cntingroup,num: integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script GroupShip');

  no:=av[1].VInt;
  num:=av[2].VInt + 1;
  cntingroup:=0;

  av[0].VDW:=0;

  cnt:=GScriptCur.FShips.Count;
  for i:=0 to cnt-1 do begin
    sship:=GScriptCur.FShips.Items[i];
    if sship.FGroup=no then begin
      inc(cntingroup);
      if cntingroup=num then av[0].VDW:=Cardinal(sship.FShip);
    end;
  end;
end;


procedure SF_ShipItems(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
  no: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script SF_ShipItems');
  ship:=TShip(av[1].VDW);
  if(ship <> nil) then begin
    if(High(av) = 1) then begin
       av[0].VInt:=ship.FEquipments.Count;
    end else begin
      no:=av[2].VInt;
      if(no >= 0) and (no < ship.FEquipments.Count) then av[0].VDW:=Cardinal(ship.FEquipments.Items[no]) else av[0].VDW:=0;
    end;
  end;
end;


procedure SF_ShipArts(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
  no: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script SF_ShipArts');
  ship:=TShip(av[1].VDW);
  if(ship <> nil) then begin
    if(High(av) = 1) then begin
       av[0].VInt:=ship.FArtefacts.Count;
    end else begin
      no:=av[2].VInt;
      if(no >= 0) and (no < ship.FArtefacts.Count) then av[0].VDW:=Cardinal(ship.FArtefacts.Items[no]) else av[0].VDW:=0;
    end;
  end;
end;


procedure SF_PlayerTranclucators(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  ship: TShip;
  i,j,counter,no,rtype:integer;
begin
  counter:=-1;
  no:=-1;
  if (High(av) >= 1) then no:=av[1].VInt;
  for i:=0 to Galaxy.FStars.Count-1 do
  begin
    star:=Galaxy.FStars.Items[i];
    for j:=0 to star.FShips.Count-1 do
    begin
      ship:=star.FShips.Items[j];
      if not (ship is TTranclucator) then continue;
      if (ship as TTranclucator).FProprietor<>Player then continue;
      inc(counter);
      if counter = no then
      begin
        av[0].VDW:=Cardinal(ship);
        exit;
      end;
    end;
  end;
  av[0].VInt:=counter+1;
end;

procedure SF_ArtTranclucatorToShip(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script SF_ArtTranclucatorToShip');
  obj:=TObject(av[1].VDW);
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if(item = nil) then Exit;
  if not(item is TArtefactTranclucator) then exit;
  av[0].VDW:=Cardinal((item as TArtefactTranclucator).FShip);
end;

procedure SF_TranclucatorData(av:array of TVarEC; code:TCodeEC);
var
  tran: TTranclucator;
  setNew:boolean;
  no:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SF_TranclucatorData');
  tran:=TTranclucator(av[1].VDW);

  if av[2].VType = vtStr then
  begin
    if      av[2].VStr = 'Proprietor' then no:=0
    else if av[2].VStr = 'ArtSize' then no:=1
    else if av[2].VStr = 'ArtSysName' then no:=2
    else if av[2].VStr = 'Docking' then no:=3
    else if av[2].VStr = 'SeekItems' then no:=4
    else if av[2].VStr = 'AutoArrange' then no:=5
    else if av[2].VStr = 'LandStorage' then no:=6
    else if av[2].VStr = 'LandPermitPlanets' then no:=7
    else if av[2].VStr = 'LandPermitRuins' then no:=8
    else if av[2].VStr = 'SeekPermitNone' then no:=9
    else if av[2].VStr = 'SeekPermitArtefact' then no:=10
    else if av[2].VStr = 'SeekPermitMicromodule' then no:=11
    else if av[2].VStr = 'SeekPermitEquipment' then no:=12
    else if av[2].VStr = 'SeekPermitUseless' then no:=13
    else if av[2].VStr = 'SeekPermitGoods' then no:=14
    else if av[2].VStr = 'SeekPermitNode' then no:=15
    else raise Exception.Create('Error.Script SF_TranclucatorData - unknown property '+av[2].VStr);
  end
  else no:=av[2].VInt;

  setNew:=(High(av)>2);

  case no of
    0: begin av[0].VDW:=Cardinal(tran.FProprietor); if setNew then tran.FProprietor:=TShip(av[3].VDW); end;
    1: begin av[0].VInt:=tran.FArtSize; if setNew then tran.FArtSize:=av[3].VInt; end;
    2: begin av[0].VStr:=tran.FArtSysName; if setNew then tran.FArtSysName:=av[3].VStr; end;
    3: begin av[0].VInt:=ord(tran.FDocking); if setNew then tran.FDocking:=av[3].VInt<>0; end;
    4: begin av[0].VInt:=ord(tran.FSeekItems); if setNew then tran.FSeekItems:=av[3].VInt<>0; end;
    5: begin av[0].VInt:=ord(tran.FAutoArrange); if setNew then tran.FAutoArrange:=av[3].VInt<>0; end;
    6: begin av[0].VInt:=ord(tran.FLandStorage); if setNew then tran.FLandStorage:=av[3].VInt<>0; end;
    7: begin av[0].VInt:=ord(tran.FLandPermit[LAND_PERMIT_PLANET]); if setNew then tran.FLandPermit[LAND_PERMIT_PLANET]:=av[3].VInt<>0; end;
    8: begin av[0].VInt:=ord(tran.FLandPermit[LAND_PERMIT_RUIN]); if setNew then tran.FLandPermit[LAND_PERMIT_RUIN]:=av[3].VInt<>0; end;
    9: begin av[0].VInt:=ord(tran.FSeekPermit[isp_None]); if setNew then tran.FSeekPermit[isp_None]:=av[3].VInt<>0; end;
    10: begin av[0].VInt:=ord(tran.FSeekPermit[isp_Artefact]); if setNew then tran.FSeekPermit[isp_Artefact]:=av[3].VInt<>0; end;
    11: begin av[0].VInt:=ord(tran.FSeekPermit[isp_Micromodule]); if setNew then tran.FSeekPermit[isp_Micromodule]:=av[3].VInt<>0; end;
    12: begin av[0].VInt:=ord(tran.FSeekPermit[isp_Equipment]); if setNew then tran.FSeekPermit[isp_Equipment]:=av[3].VInt<>0; end;
    13: begin av[0].VInt:=ord(tran.FSeekPermit[isp_Useless]); if setNew then tran.FSeekPermit[isp_Useless]:=av[3].VInt<>0; end;
    14: begin av[0].VInt:=ord(tran.FSeekPermit[isp_Goods]); if setNew then tran.FSeekPermit[isp_Goods]:=av[3].VInt<>0; end;
    15: begin av[0].VInt:=ord(tran.FSeekPermit[isp_Node]); if setNew then tran.FSeekPermit[isp_Node]:=av[3].VInt<>0; end;
    else raise Exception.Create('Error.Script SF_TranclucatorData - unknown property '+inttostrec(no));
  end;
end;


procedure SF_LinkItemToScript(av:array of TVarEC; code:TCodeEC);
var
  sitem: TScriptItem;
  item: TItem;
  i:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script SF_LinkItemToScript');

  item:=TItem(av[1].VDW);
  if(item.FScriptItem <> nil) then (item.FScriptItem as TScriptItem).FItem:=nil;

  if(High(av) < 2) then
  begin
    if GScriptCur=nil then raise Exception.Create('Error.Script SF_LinkItemToScript - no script');
    sitem:=nil;
    for i:=0 to GScriptCur.FItem.Count-1 do
    begin
      sitem:=GScriptCur.FItem[i];
      if (sitem.FName='') and (sitem.FItem=nil) then break;
      sitem:=nil;
    end;
    if sitem=nil then
    begin
      sitem:=TScriptItem.Create;
      GScriptCur.FItem.Add(sitem);
    end;
    if sitem.FOnActCompiledCode<>nil then sitem.FOnActCompiledCode.Free;
    sitem.FOnActCompiledCode:=nil;
    sitem.FOnActCode:='';
    
  end else begin
    sitem:=TScriptItem(av[2].VDW);
  end;

  if(sitem.FItem <> nil) then sitem.FItem.FScriptItem:=nil;
   
  sitem.FItem:=item;
  item.FScriptItem:=sitem;
end;


procedure SF_ReleaseItemFromScript(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  sitem: TScriptItem;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ReleaseItemFromScript');
  obj:=TObject(av[1].VDW);
  sitem:=nil;
  if(obj is TItem) then sitem:=TScriptItem(TItem(obj).FScriptItem);
  if(obj is TScriptItem) then sitem:=TScriptItem(obj);
  
  if(sitem.FItem <> nil) then sitem.FItem.FScriptItem:=nil;
  sitem.FItem:=nil;
end;

procedure SF_ScriptItemData(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  flag: Boolean;
  sitem: TScriptItem;
  no:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ScriptItemData');
  obj:=TObject(av[1].VDW);
  sitem:=nil;
  if obj is TItem then sitem:=TScriptItem(TItem(obj).FScriptItem);
  if obj is TScriptItem then sitem:=TScriptItem(obj);
  av[0].VInt:=0;
  no:=av[2].VInt;
  case no of
    1: av[0].VInt:=sitem.FData1;
    2: av[0].VInt:=sitem.FData2;
    3: av[0].VInt:=sitem.FData3;
    else raise Exception.Create('Error.Script ScriptItemData no');
  end;

  if (High(av) > 2) then
  case no of
    1: sitem.FData1:=av[3].VInt;
    2: sitem.FData2:=av[3].VInt;
    3: sitem.FData3:=av[3].VInt;
  end;

end;

procedure SF_ScriptItemTextData(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  flag: Boolean;
  sitem: TScriptItem;
  no:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ScriptItemTextData');
  obj:=TObject(av[1].VDW);
  sitem:=nil;
  if obj is TItem then sitem:=TScriptItem(TItem(obj).FScriptItem);
  if obj is TScriptItem then sitem:=TScriptItem(obj);
  av[0].VStr:='';
  no:=av[2].VInt;
  case no of
    1: av[0].VStr:=sitem.FTextData1;
    2: av[0].VStr:=sitem.FTextData2;
    3: av[0].VStr:=sitem.FTextData3;
    else raise Exception.Create('Error.Script ScriptItemTextData no');
  end;

  if (High(av) > 2) then
  case no of
    1: sitem.FTextData1:=av[3].VStr;
    2: sitem.FTextData2:=av[3].VStr;
    3: sitem.FTextData3:=av[3].VStr;
  end;

end;

procedure SF_ScriptItemToItem(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ScriptItemToItem');
  obj:=TObject(av[1].VDW);
  av[0].VDW:=0;
  if obj=nil then exit;
  if obj is TItem then
  begin
    av[0].VDW:=Cardinal(obj);
    exit;
  end;
  if not (obj is TScriptItem) then exit;
  av[0].VDW:=Cardinal(TScriptItem(obj).FItem);
end;

procedure SF_GetShipPirateRank(av:array of TVarEC; code:TCodeEC);
var
  ship: TNormalShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script GetShipPirateRank');
  ship:=TNormalShip(av[1].VDW);
  av[0].VDW:=Cardinal(ship.FPirateRank);
end;

procedure SF_ShipPirateRankPoints(av:array of TVarEC; code:TCodeEC);
var
    ship:TNormalShip;
begin
    if High(av)<1 then raise Exception.Create('Error.Script ShipPirateRankPoints');
    ship:=TShip(av[1].VDW) as TNormalShip;
    av[0].VDW:=integer(ship.FPirateRankPoints);
    if High(av)>1 then ship.FPirateRankPoints:=av[2].VDW;
end;

procedure SF_ShipNextPirateRankPoints(av:array of TVarEC; code:TCodeEC);
var
    ship:TNormalShip;
begin
    if High(av)<1 then raise Exception.Create('Error.Script ShipNextPirateRankPoints');
    ship:=TShip(av[1].VDW) as TNormalShip;
    av[0].VInt:=integer(mPirateRank[ship.FPirateRank]);
end;


procedure SF_ShipInPirateClan(av:array of TVarEC; code:TCodeEC);
var
  ship: TNormalShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipInPirateClan');
  ship:=TNormalShip(av[1].VDW);
  if ship=Player then av[0].VDW:=Cardinal(Player.FPirateClanReal) else
    av[0].VDW:=Cardinal(ship.FOwner=PirateClan);
end;

procedure SF_ShipOnSidePirateClan(av:array of TVarEC; code:TCodeEC);
var
  ship: TNormalShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipOnSidePirateClan');
  ship:=TNormalShip(av[1].VDW);
  av[0].VDW:=Cardinal(ship.FOwner=PirateClan);
end;


procedure SF_RaisePirateRank(av:array of TVarEC; code:TCodeEC);
var
  ship: TNormalShip;
  rank: Cardinal;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script RaisePirateRank');
  ship:=TNormalShip(av[1].VDW);
  rank:=Cardinal(ship.FPirateRank);
  if(rank < 7) then ship.FPirateRank:=TPirateRank(rank+1);
  if ship=Player then Player.FAchievementStats.CheckConditionAchBaron();
end;


procedure SF_ItemType(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  itemtype: TItemType;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemType');
  itemtype:=TItemType(0);
  obj:=TObject(av[1].VDW);
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if(item <> nil) then itemtype:=item.FItemType;
  av[0].VDW:=Cardinal(itemtype);
end;

procedure SF_CustomWeaponType(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  itemtype: TItemType;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script CustomWeaponType');
  av[0].VStr:='';
  obj:=TObject(av[1].VDW);
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if(item <> nil) and (item is TCustomWeapon) then av[0].VStr:=(item as TCustomWeapon).WeaponInfo.SysName;
end;


procedure SF_ItemName(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  s: WideString;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemName');
  obj:=TObject(av[1].VDW);
  item:=nil;
  s:='';
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if(item <> nil) then s:=item.ShortName;
  av[0].VStr:=s;
end;

procedure SF_ItemFullName(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  s: WideString;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemFullName');
  obj:=TObject(av[1].VDW);
  item:=nil;
  s:='';
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if(item <> nil) then s:=item.Name;
  av[0].VStr:=s;
end;

procedure SF_ItemSize(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  size,newsize: integer;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemSize');
  size:=0;
  obj:=TObject(av[1].VDW);
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if(item <> nil) then begin
    size:=item.FSize;
    if(High(av) > 1) then
    begin
      newsize:=av[2].VInt;
      if item is TCountableItem then
      begin
        item.FCost := round(item.FCost * newsize / max(1,item.FSize));
        (item as TCountableItem).FCount := newsize;
      end;
      if item.FItemType in Goods then
      begin
        item.FCost := round(item.FCost * newsize / max(1,item.FSize));
        (item as TGoods).FCount := newsize;
      end;
      item.FSize:=av[2].VInt;
    end;
  end else if obj is TTranclucator then
  begin
    size:=(obj as TTranclucator).FArtSize;
    if (High(av) > 1) then (obj as TTranclucator).FArtSize:=av[2].VInt;
  end;
  av[0].VDW:=Cardinal(size);
end;


procedure SF_ItemOwner(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  owner: TOwner;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemOwner');
  owner:=TOwner(0);
  obj:=TObject(av[1].VDW);
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if(item <> nil) then begin
    owner:=item.FOwner;
    if(High(av) > 1) then item.FOwner:=TOwner(av[2].VDW);
  end;
  av[0].VDW:=Cardinal(owner);
end;


procedure SF_ItemSubrace(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  subrace: TDominatorSeries;
  item: TEquipment;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemSubrace');
  subrace:=TDominatorSeries(0);
  obj:=TObject(av[1].VDW);
  item:=nil;
  if(obj is TItem) then item:=TEquipment(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem as TEquipment;
  if(item <> nil) then begin
    subrace:=item.FDS;
    if(High(av) > 1) then item.FDS:=TDominatorSeries(av[2].VDW);
  end;
  av[0].VDW:=Cardinal(subrace);
end;


procedure SF_ItemCost(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  cost: integer;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemCost');
  cost:=0;
  obj:=TObject(av[1].VDW);
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if(item <> nil) then begin
    cost:=item.FCost;
    if(High(av) > 1) then item.FCost:=av[2].VInt;
  end;
  av[0].VDW:=Cardinal(cost);
end;


procedure SF_ItemIsInUse(av:array of TVarEC; code:TCodeEC);
var
  obj:  TObject;
  item: TItem;
  ship: TShip;
  i:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemIsInUse');
  obj:=TObject(av[1].VDW);
  av[0].VInt:=0;
  item:=nil;
  if obj is TItem then item:=TItem(obj);
  if obj is TScriptItem then item:=TScriptItem(obj).FItem;
  if item=nil then exit;

  if (item is TEquipment) and (item as TEquipment).FExplotable then av[0].VInt:=(item as TEquipment).FSlot+1;

  if (High(av) > 2) and (item is TEquipment) then
  begin
    ship:=TShip(av[2].VDW);
    if ship=nil then exit;
    if item is TArtefact then
    begin
      if av[3].VInt<>0 then
      begin
        TArtefact(item).Activate;
        if High(av) > 3 then TArtefact(item).FSlot:=av[4].VInt-1;
      end
      else (item as TArtefact).DeActivate;
    end
    else if item is TWeapon then
    begin
      if av[3].VInt<>0 then
      begin
        ship.Activate(TEquipment(item));
        if High(av) > 3 then TEquipment(item).FSlot:=av[4].VInt-1;
      end
      else begin
        for i:=1 to ship.FWeaponCnt do if ship.FWeapon[i]=item then ship.DeActivate(item.FItemType,i);
      end;
    end
    else
    begin
      if av[3].VInt<>0 then
       begin
        ship.Activate(TEquipment(item));
        if High(av) > 3 then TEquipment(item).FSlot:=av[4].VInt-1;
      end
      else ship.DeActivate(item.FItemType);
    end;
    ship.SlotCorrect;
    ship.CalcParam;
    ship.ScriptItemsAct(t_OnNonStandartEqChange);
  end;
end;

procedure SF_ItemIsInSet(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
  i,j:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemIsInSet');
  obj:=TObject(av[1].VDW);
  item:=nil;
  av[0].VInt:=0;
  if obj is TItem then item:=TItem(obj);
  if obj is TScriptItem then item:=TScriptItem(obj).FItem;
  if item = nil then Exit;

  if High(av) > 1 then
  begin
    i:=av[2].VInt-1;
    if (i<0) or (i>High(Player.FHotEquipments)) then exit;

    for j := 0 to High(Player.FHotEquipments[i].EquId) do
      if Player.FHotEquipments[i].EquId[j] = item.FId then
      begin
        av[0].VInt:=1;
        Exit;
      end;

    exit;
  end;

  for i := 0 to High(Player.FHotEquipments) do
  begin
    for j := 0 to High(Player.FHotEquipments[i].EquId) do
      if Player.FHotEquipments[i].EquId[j] = item.FId then
      begin
        av[0].VInt:=i+1;
        Exit;
      end;
    for j := 0 to High(Player.FHotEquipments[i].ArtId) do
      if Player.FHotEquipments[i].ArtId[j] = item.FId then
      begin
        av[0].VInt:=i+1;
        Exit;
      end;
  end;
end;

procedure SF_PlayerEqSet(av:array of TVarEC; code:TCodeEC);
var no:integer;
begin
  if(High(av) < 1) then // no args - returns active set
  begin
    av[0].VInt:=Player.FHotEquipmentCur+1;
    exit;
  end;

  // ont arguments - checks set N
  no:=av[1].VInt-1;
  if Player.FHotEquipmentCur = no then av[0].VInt:=2
  else if Player.IsExistHotEquipments(no) then av[0].VInt:=1  //0 - not defined, 1 - defined, 2 - active
  else av[0].VInt:=0;
end;


procedure SF_ItemIsBroken(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  flag: Boolean;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemIsBroken');
  obj:=TObject(av[1].VDW);
  flag:=false;
  item:=nil;
  if obj is TItem then item:=TItem(obj);
  if obj is TScriptItem then item:=TScriptItem(obj).FItem;
  if(item <> nil) then begin
    if(item is TEquipment) then flag:=(item as TEquipment).FBroken;
    if(item is TArtefact) then flag:=(item as TArtefact).FBroken;
  end;
  if flag then av[0].VInt:=1
  else av[0].VInt:=0;
end;


procedure SF_ShipCanUseEq(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
  ship: TShip;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ShipCanUseEq');
  ship:=TShip(av[1].VDW);
  obj:=TObject(av[2].VDW);

  if obj is TItem then item:=TItem(obj)
  else if obj is TScriptItem then item:=TScriptItem(obj).FItem
  else item:=nil;

  av[0].VInt:=0;

  if (item = nil) or not (item is TEquipment) then exit;

  av[0].VInt:=ord(ship.KnowsHowToUse(TEquipment(item)));
end;


procedure SF_ShipCanRepairEq(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
  ship: TShip;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ShipCanRepairEq');
  ship:=TShip(av[1].VDW);
  obj:=TObject(av[2].VDW);

  if obj is TItem then item:=TItem(obj)
  else if obj is TScriptItem then item:=TScriptItem(obj).FItem
  else item:=nil;

  av[0].VInt:=0;

  if (item = nil) or not (item is TEquipment) then exit;

  av[0].VInt:=ord(ship.KnowsHowToRepair(TEquipment(item)));
end;


procedure SF_ShipTechLevelKnowledge(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipTechLevelKnowledge');
  ship:=TShip(av[1].VDW);
  av[0].VInt:=ship.FTechLevelKnowledge;
  if High(av) > 1 then ship.FTechLevelKnowledge:=av[2].VInt;
end;


procedure SF_WeaponTarget(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script WeaponTarget');
  obj:=TObject(av[1].VDW);
  av[0].VDW:=0;

  item:=nil;
  if obj is TItem then item:=TItem(obj);
  if obj is TScriptItem then item:=TScriptItem(obj).FItem;

  if item = nil then Exit;
  if not(item is TWeapon) then Exit;
  if not(item as TWeapon).FExplotable then Exit;

  av[0].VDW:=Cardinal((item as TWeapon).FTarget);
  if High(av) > 1 then (item as TWeapon).FTarget:=TObject(av[2].VDW);

end;

procedure SF_GetEquipmentStats(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
  datatype:integer;
  tstr:WideString;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script GetEquipmentStats');
  obj:=TObject(av[1].VDW);
  datatype:=0;


  item:=nil;
  if obj is TItem then item:=TItem(obj);
  if obj is TScriptItem then item:=TScriptItem(obj).FItem;

  if item = nil then Exit;

  if High(av) > 1 then
  begin
    if av[2].VType = vtStr then
    begin
      if item is TEquipment then
      begin
        tstr:=av[2].VStr;
        TEquipment(item).FillStats(tstr);
        av[0].VStr:=tstr;
      end
      else av[0].VStr:='';
      exit;
    end;
    datatype:=av[2].VInt;
    av[0].VInt:=0;
  end;

  if item.FItemType in Weapons then
  begin
    case datatype of
      0: av[0].VInt := (item as TWeapon).FMaxDamage;
      1: av[0].VInt := (item as TWeapon).FMinDamage;
      2: av[0].VInt := (item as TWeapon).FRadius;

      //read only
      3: av[0].VInt := integer(PrimaryDamageType((item as TWeapon).WeaponInfo.DamageType));
      4: av[0].VInt := (item as TWeapon).AttackCount;
      5: av[0].VInt := (item as TWeapon).ShotCount;
      6: av[0].VDW  := cardinal((item as TWeapon).DamageType);
    end;
  end else begin
    case item.FItemType of
      t_Hull:
      begin
        case datatype of
          0: av[0].VInt := (item as THull).FHitProtect;

          //read only
          1: av[0].VInt := (item as THull).SlotCount(st_Weapon);
          2: av[0].VInt := (item as THull).SlotCount(st_Artefact);
          3: av[0].VInt := (item as THull).SlotCount(st_Radar);
          4: av[0].VInt := (item as THull).SlotCount(st_Scaner);
          5: av[0].VInt := (item as THull).SlotCount(st_RepairRobot);
          6: av[0].VInt := (item as THull).SlotCount(st_CargoHook);
          7: av[0].VInt := (item as THull).SlotCount(st_DefGenerator);
          8: av[0].VInt := (item as THull).SlotCount(st_Forsage);
        end;
      end;
      t_FuelTanks:
      begin
        case datatype of
          0: av[0].VInt := (item as TFuelTanks).FCapacity;
          1: av[0].VInt := (item as TFuelTanks).FFuel;
        end;
      end;
      t_Engine:
      begin
        case datatype of
          0: av[0].VInt := (item as TEngine).FSpeed;
          1: av[0].VInt := (item as TEngine).FParsec;
        end;
      end;
      t_Radar: av[0].VInt := (item as TRadar).FRadius;
      t_Scaner: av[0].VInt := (item as TScaner).FScanProtect;
      t_RepairRobot: av[0].VInt := (item as TRepairRobot).FRecoverHitPoints;
      t_CargoHook:
      begin
        case datatype of
          0: av[0].VInt := (item as TCargoHook).FPickUpSize;
          1: av[0].VInt := (item as TCargoHook).FHookRadius;
          2: av[0].VFloat := (item as TCargoHook).FSpeedMin;
          3: av[0].VFloat := (item as TCargoHook).FSpeedMax;
        end;
      end;
      t_DefGenerator: av[0].VInt := round(100-100*(item as TDefGenerator).FDefFactor);
      t_Cistern:
      begin
        case datatype of
          0: av[0].VInt := (item as TCistern).FCapacity;
          1: av[0].VInt := (item as TCistern).FFuel;
        end;
      end;
      t_Satellite:
      begin
        case datatype of
          0: av[0].VInt := (item as TSatellite).FWaterSpeed;
          1: av[0].VInt := (item as TSatellite).FLandSpeed;
          2: av[0].VInt := (item as TSatellite).FHillSpeed;
          3: av[0].VFloat := (item as TSatellite).FWear;
        end;
      end;
    end;
  end;
end;

procedure SF_SetEquipmentStats(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
  datatype,value:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SetEquipmentStats');
  obj:=TObject(av[1].VDW);
  value:=av[2].VDW;
  datatype:=0;
  if(High(av) > 2) then datatype:=av[3].VInt;

  item:=nil;
  if obj is TItem then item:=TItem(obj);
  if obj is TScriptItem then item:=TScriptItem(obj).FItem;

  if item = nil then Exit;

  if item.FItemType in Weapons then
  begin
    case datatype of
      0: (item as TWeapon).FMaxDamage := value;
      1: (item as TWeapon).FMinDamage := value;
      2: (item as TWeapon).FRadius := value;
    end;
  end else begin
    case item.FItemType of
      t_Hull: (item as THull).FHitProtect := value;
      t_FuelTanks:
      begin
        case datatype of
          0: (item as TFuelTanks).FCapacity := value;
          1: (item as TFuelTanks).FFuel := value;
        end;
      end;
      t_Engine:
      begin
        case datatype of
          0: (item as TEngine).FSpeed := value;
          1: (item as TEngine).FParsec := value;
        end;
      end;
      t_Radar: (item as TRadar).FRadius := value;
      t_Scaner: (item as TScaner).FScanProtect := value;
      t_RepairRobot: (item as TRepairRobot).FRecoverHitPoints := value;
      t_CargoHook:
      begin
        case datatype of
          0: (item as TCargoHook).FPickUpSize := value;
          1: (item as TCargoHook).FHookRadius := value;
          2: (item as TCargoHook).FSpeedMin:=av[2].VFloat;
          3: (item as TCargoHook).FSpeedMax:=av[2].VFloat;
        end;
      end;
      t_DefGenerator: (item as TDefGenerator).FDefFactor := (100 - value)*0.01;
      t_Cistern:
      begin
        case datatype of
          0: (item as TCistern).FCapacity := value;
          1: (item as TCistern).FFuel := value;
        end;
      end;
      t_Satellite:
      begin
        case datatype of
          0: (item as TSatellite).FWaterSpeed := value;
          1: (item as TSatellite).FLandSpeed := value;
          2: (item as TSatellite).FHillSpeed := value;
          3: (item as TSatellite).FWear := av[2].VFloat;
        end;
      end;
    end;
  end;
end;


procedure SF_CreateHull(av:array of TVarEC; code:TCodeEC);
var
  hull: THull;
  hulltype: TItemType;
  owner: TOwner;
  level: integer;
  size: integer;
  series: integer;
  pirateBuilt:boolean;
begin
  if(High(av) < 4) then raise Exception.Create('Error.Script CreateHull');
  hulltype:=TItemType(av[1].VDW);
  size:=av[2].VInt;
  level:=av[3].VInt;
  owner:=TOwner(av[4].VDW);
  series:=NoSeries;
  pirateBuilt:=false;
  if High(av) > 4 then series:=av[5].VInt;
  if High(av) > 5 then pirateBuilt:=(av[6].VInt<>0);

  hull:=THull.Create;
  hull.Init(size, TTechLevel(level), owner, TSShipType(hulltype), series, pirateBuilt);
  av[0].VDW:=Cardinal(hull);
end;


procedure SF_CreateEquipment(av:array of TVarEC; code:TCodeEC);
var
  item: TItem;
  itemtype: TItemType;
  owner: TOwner;
  size,level: integer;
begin
  if(High(av) < 4) then raise Exception.Create('Error.Script CreateEquipment');
  itemtype:=TItemType(av[1].VDW);
  size:=av[2].VInt;
  level:=av[3].VInt;
  owner:=TOwner(av[4].VDW);

  if itemtype=t_Cistern then
  begin
    item:=TCistern.Create;
    TCistern(item).Init(level,size,owner);//level->fuel
  end
  else item:=CreateEq(itemtype,size,TTechLevel(level),owner);

  av[0].VDW:=Cardinal(item);
end;


procedure SF_CreateArt(av:array of TVarEC; code:TCodeEC);
var
  item: TItem;
  itemtype: TItemType;
  owner: TOwner;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script CreateArt');
  itemtype:=TItemType(av[1].VDW);
  owner:=TOwner(av[2].VDW);
  item:=ArtefactCreate(itemtype, owner);
  av[0].VDW:=Cardinal(item);
end;

procedure SF_CreateCustomWeapon(av:array of TVarEC; code:TCodeEC);
var
  item: TItem;
  owner: TOwner;
  size,level: integer;
  winfo:PWeaponInfo;
begin
  if(High(av) < 4) then raise Exception.Create('Error.Script CreateEquipment');
  winfo:=Galaxy.GetCustomWeaponInfo(av[1].VStr);
  size:=av[2].VInt;
  level:=av[3].VInt;
  owner:=TOwner(av[4].VDW);
  item:=CreateWeapon(winfo,size,TTechLevel(level),owner);
  av[0].VDW:=Cardinal(item);
end;


procedure SF_CreateCustomArt(av:array of TVarEC; code:TCodeEC);
var
  item: TArtefactCustom;
  name: WideString;
  owner: TOwner;
  size,cost:integer;
begin
  if(High(av) < 4) then raise Exception.Create('Error.Script CreateCustomArt');
  name:=av[1].VStr;
  size:=av[2].VInt;
  cost:=av[3].VInt;
  owner:=TOwner(av[4].VDW);
  item:=TArtefactCustom.Create;
  item.InitEx(name,size,cost,owner);
  av[0].VDW:=Cardinal(item);
end;

procedure SF_CustomArtData(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  flag: Boolean;
  item: TItem;
  no:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script CustomArtData');
  obj:=TObject(av[1].VDW);
  item:=nil;
  if obj is TItem then item:=TItem(obj);
  if obj is TScriptItem then item:=TScriptItem(obj).FItem;
  av[0].VInt:=0;
  if not (item is TArtefactCustom) then exit;
  no:=av[2].VInt;
  case no of
    1: av[0].VInt:=(item as TArtefactCustom).FData1;
    2: av[0].VInt:=(item as TArtefactCustom).FData2;
    3: av[0].VInt:=(item as TArtefactCustom).FData3;
    else raise Exception.Create('Error.Script CustomArtData no');
  end;

  if (High(av) > 2) then
  case no of
    1: (item as TArtefactCustom).FData1:=av[3].VInt;
    2: (item as TArtefactCustom).FData2:=av[3].VInt;
    3: (item as TArtefactCustom).FData3:=av[3].VInt;
  end;

end;

procedure SF_CustomArtTextData(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  flag: Boolean;
  item: TItem;
  no:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script CustomArtTextData');
  obj:=TObject(av[1].VDW);
  item:=nil;
  if obj is TItem then item:=TItem(obj);
  if obj is TScriptItem then item:=TScriptItem(obj).FItem;
  av[0].VStr:='';
  if not (item is TArtefactCustom) then exit;
  no:=av[2].VInt;
  case no of
    1: av[0].VStr:=(item as TArtefactCustom).FTextData1;
    2: av[0].VStr:=(item as TArtefactCustom).FTextData2;
    3: av[0].VStr:=(item as TArtefactCustom).FTextData3;
    else raise Exception.Create('Error.Script CustomArtTextData no');
  end;

  if (High(av) > 2) then
  case no of
    1: (item as TArtefactCustom).FTextData1:=av[3].VStr;
    2: (item as TArtefactCustom).FTextData2:=av[3].VStr;
    3: (item as TArtefactCustom).FTextData3:=av[3].VStr;
  end;

end;

procedure SF_CreateMM(av:array of TVarEC; code:TCodeEC);
var
  num: integer;
  mm: TMicroModule;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script CreateMM');
  num:=av[1].VInt;
  mm:=TMicroModule.Create;
  mm.Init(num);
  av[0].VDW:=Cardinal(mm);
end;

procedure SF_CreateNodes(av:array of TVarEC; code:TCodeEC);
var
  nodes: TProtoplasm;
  natural:boolean;
  ser:TDominatorSeries;
  num:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script CreateNodes');
  num:=av[1].VInt;
  natural:=false;
  ser:=t_Blazer;
  if (High(av) > 1) then ser:=TDominatorSeries(av[2].VInt);
  if (High(av) > 2) then natural:=av[3].VInt <> 0;
  nodes:=TProtoplasm.Create;
  nodes.Init(num,natural);
  nodes.FDS:=ser;
  av[0].VDW:=Cardinal(nodes);
end;

procedure SF_CreateCustomCountableItem(av:array of TVarEC; code:TCodeEC);
var
  name:WideString;
  cnt:integer;
  natural:boolean;
  item:TCountableItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script CreateCustomCountableItem');
  name:=av[1].VStr;// points to block Lang.dat Items.CustomCountables.name
  if(High(av) > 1) then cnt:=av[2].VInt else cnt:=1;
  if(High(av) > 2) then natural:=av[3].VInt<>0 else natural:=false;
  item:=TCountableItem.Create;
  item.Init(name,cnt,natural);
  av[0].VDW:=Cardinal(item);
end;


procedure SF_CreateZond(av:array of TVarEC; code:TCodeEC);
var
  satellite: TSatellite;
  owner: TOwner;
  level: byte;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script CreateZond');
  level:=byte(av[1].VDW);
  owner:=TOwner(av[2].VDW);

  satellite:=TSatellite.Create;
  satellite.Init(level, owner, RndOut(1,10000,Galaxy.FRndOut));

  if(High(av) > 4) then begin
    satellite.FWaterSpeed:=byte(av[3].VInt);
    satellite.FLandSpeed:=byte(av[4].VInt);
    satellite.FHillSpeed:=byte(av[5].VInt);
  end;

  av[0].VDW:=Cardinal(satellite);
end;

procedure SF_ExistingZonds(av:array of TVarEC; code:TCodeEC);
var
  no: integer;
begin
  if High(av) < 1 then
  begin
    av[0].VInt := Galaxy.SatelliteInGame;
    exit;
  end;

  no:=av[1].VInt;
  if (no>=0) and (no<Player.FSatellite.Count) then
  begin
    if (High(av) > 1) and (av[2].VInt=1) then av[0].VDW:=Cardinal(TSatellite(Player.FSatellite[no]).FPlanet)
    else av[0].VDW:=Cardinal(Player.FSatellite[no]);
  end else av[0].VDW:=0;
end;


procedure SF_FreeItem(av:array of TVarEC; code:TCodeEC);
var
  item: TItem;
  obj: TObject;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script FreeItem');
  obj:=TObject(av[1].VDW);
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if item<>nil then begin
   if(item.FScriptItem <> nil) then (item.FScriptItem as TScriptItem).FItem:=nil;
   item.Free;
  end;
end;


procedure SF_ShipJoinsClan(av:array of TVarEC; code:TCodeEC);
var
  ship: TNormalShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipJoinsClan');
  ship:=TNormalShip(av[1].VDW);
  ship.FOwner:=PirateClan;
  if ship=Player then Player.FPirateClanReal:=true;
end;


procedure SF_AddItemToShip(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
  item,item2: TItem;
  gtype: TItemType;
  i:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script AddItemToShip');
  ship:=TShip(av[1].VDW);
  item:=TItem(av[2].VDW);
  if(item is TGoods) then begin
    gtype:=(item as TGoods).FItemType;
    ship.FGoods[gtype].Cnt:=ship.FGoods[gtype].Cnt+(item as TGoods).FSize;
    ship.FGoods[gtype].Cost:=ship.FGoods[gtype].Cost+item.FCost;
    item.Free;
  end else if(item is TCountableItem) then
  begin
    for i:=1 to ship.FEquipments.Count-1 do
    begin
      item2:=ship.FEquipments.Items[i];
      if (item as TCountableItem).CanCombineWith(item2) then
       begin
         (item2 as TCountableItem).CombineWith(item);
         item.Free;
         item:=nil;//note that this can invalidate countable item pointer
         break;
       end;
    end;
    if item<>nil then ship.FEquipments.Add(item);
  end else if(item is THull) and (ship.FHull=nil) then
  begin
    ship.FEquipments.Insert(0,item);
    ship.Activate(THull(item));
    THull(item).FShip:=ship;
    ship.SlotCorrect;
    ship.CalcParam;
    ship.ScriptItemsAct(t_OnNonStandartEqChange);

  end else if(item is TArtefact) then ship.FArtefacts.Add(item)
  else if(item is TEquipment) then ship.FEquipments.Add(item);
end;


procedure SF_GetItemFromShip(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
  item: TItem;
  no,i: integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script GetItemFromShip');

  ship:=TShip(av[1].VDW);
  av[0].VDW:=0;
  if ship = nil then exit;

  if (av[2].VType = vtDW) and (av[2].VDW > 65536) then
  begin
    item:=TItem(av[2].VDW);
    no:=ship.FEquipments.IndexOf(item);
    if no<0 then exit;
  end else begin
    no:=av[2].VInt;
    if(no < 0) or (no >= ship.FEquipments.Count) then exit;
    item:=ship.FEquipments.Items[no];
  end;

  av[0].VDW:=Cardinal(item);
  if ship.FHull = item then
  begin
    ship.FHull.FShip:=nil;
    ship.DeActivate(t_Hull);

  end else if(item is TEquipment) and (item as TEquipment).FExplotable then
  begin
    if(item.FItemType in EqInSlot) then ship.DeActivate(item.FItemType);
    if(item is TWeapon) then
    begin
      for i:=1 to ship.WeaponCnt do
      if(ship.FWeapon[i]=item) then
      begin
        ship.DeActivate(BasicWeapon,i);
        break;
      end;
    end;
  end;
  ship.FEquipments.Delete(no);
end;


procedure SF_GetArtFromShip(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
  ar :TArtefact;
  no: integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script GetArtFromShip');

  ship:=TShip(av[1].VDW);
  av[0].VDW:=0;
  if ship = nil then exit;

  if (av[2].VType = vtDW) and (av[2].VDW > 65536) then
  begin
    ar:=TArtefact(av[2].VDW);
    no:=ship.FArtefacts.IndexOf(ar);
    if no<0 then exit;
  end else begin
    no:=av[2].VInt;
    if(no < 0) or (no >= ship.FArtefacts.Count) then exit;
    ar:=ship.FArtefacts.Items[no];
  end;

  ar.DeActivate;
  av[0].VDW:=Cardinal(ar);
  ship.FArtefacts.Delete(no);
end;

procedure SF_ArrangeItems(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ArrangeItems');
  ship:=TShip(av[1].VDW);
  ship.ArrangeEquipments;
  ship.ArrangeArtefacts;
  ship.DropWasteItems;
  ship.SlotCorrect;
end;

procedure SF_AddItemToPlanet(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  item: TItem;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script AddItemToPlanet');
  planet:=TPlanet(av[1].VDW);
  item:=TItem(av[2].VDW);
  av[0].VInt:=0;
  if(planet <> nil) and (item <> nil) then begin
    if planet.ItemPutToPlanet(item) then av[0].VInt:=1;
  end;
end;


procedure SF_GetItemFromPlanet(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  goneitem: PGoneItem;
  no: integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script GetItemFromPlanet');
  planet:=TPlanet(av[1].VDW);
  no:=av[2].VInt;
  av[0].VDW:=0;
  if(planet <> nil) then
  begin
    if planet.FGoneItems = nil then exit;
    if(no >= 0) and (no < planet.FGoneItems.Count) then
    begin
      goneitem:=planet.FGoneItems.Items[no];
      av[0].VDW:=Cardinal(goneitem.FItem);
      planet.FGoneItems.Delete(no);
      goneitem.FItem:=nil;
      Dispose(goneitem);
    end;
  end;
end;


procedure SF_AddItemToShop(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TEquipment;
  updateshop: boolean;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script AddItemToShop');
  obj:=TObject(av[1].VDW);
  item:=TEquipment(av[2].VDW);
  av[0].VInt:=0;

  updateshop:=(GShopList <> nil) and ((Player.FCurPlanet = obj) or (Player.FCurShip = obj));

  if(item <> nil) then begin
    if(obj is TPlanet) then begin
      if updateshop then ShopListToEquipmentShop(); // ????????????? ???? ? ???????
      (obj as TPlanet).FEquipmentShop.Add(item);
      av[0].VInt:=1;
      if updateshop then begin
        EquipmentShopToShopList(); // ????????????? ???? ? ???????
        GFormEquipmentShop.FreeImage();
        GFormEquipmentShop.BuildImage();
        GFormEquipmentShop.UpdateT();
      end;
    end else if(obj is TRuins) then begin
      if updateshop then ShopListToEquipmentShop(); // ????????????? ???? ? ????
      (obj as TRuins).FEquipmentShop.Add(item);
      av[0].VInt:=1;
      if updateshop then begin
        EquipmentShopToShopList(); // ????????????? ???? ? ???????
        GFormEquipmentShop.FreeImage();
        GFormEquipmentShop.BuildImage();
        GFormEquipmentShop.UpdateT();
      end;
    end;
  end;
end;


procedure SF_GetItemFromShop(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  no: integer;
  updateshop: boolean;
  eqShop:TObjectList;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script GetItemFromShop');
  obj:=TObject(av[1].VDW);
  av[0].VDW:=0;

  if obj = nil then exit;
  updateshop:=(GShopList <> nil) and ((Player.FCurPlanet = obj) or (Player.FCurShip = obj));
  if updateshop then fEquipmentShop.ShopListToEquipmentShop();

  if obj is TPlanet then eqShop:=TPlanet(obj).FEquipmentShop
  else if obj is TRuins then eqShop:=TRuins(obj).FEquipmentShop
  else exit;

  if (av[2].VType = vtDW) and (av[2].VDW > 65536) then
  begin
    no:=eqShop.IndexOf(TItem(av[2].VDW));
    if no >= 0 then
    begin
      av[0].VDW:=av[2].VDW;
      eqShop.Delete(no);
    end;
  end else begin
    no:=av[2].VInt;
    if (no >= 0) and (no < eqShop.Count) then
    begin
      av[0].VDW:=Cardinal(eqShop.Items[no]);
      eqShop.Delete(no);
    end;
  end;

  if updateshop then
  begin
    EquipmentShopToShopList();
    GFormEquipmentShop.FreeImage();
    GFormEquipmentShop.BuildImage();
    GFormEquipmentShop.UpdateT();
  end;
end;


procedure SF_AddItemToStorage(av:array of TVarEC; code:TCodeEC);
var
  i:integer;
  obj: TObject;
  item: TItem;
  su: PStorageUnit;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script AddItemToStorage');
  obj:=TObject(av[1].VDW);
  item:=TItem(av[2].VDW);
  av[0].VInt:=0;

  if item is TGoods then for i:=0 to Player.FStorage.Count-1 do
  begin
    su:=Player.FStorage.Items[i];
    if su.FPlace <> Obj then continue;
    if not (su.FItem is TGoods) then continue;
    with su.FItem as TGoods do
    begin
      if FItemType <> item.FItemType then continue;
      FCount:=FCount+TGoods(item).FCount;
      FSize:=FSize+item.FSize;
      FCost:=FCost+item.FCost;
    end;
    item.Free;
    av[0].VInt:=i;
    Player.StorageToMsgPlayer();
    exit;
  end;

  if item is TCountableItem then for i:=0 to Player.FStorage.Count-1 do
  begin
    su:=Player.FStorage.Items[i];
    if su.FPlace <> Obj then continue;
    if not (su.FItem is TCountableItem) then continue;
    with su.FItem as TCountableItem do
    begin
      if not CanCombineWith(item) then continue;
      CombineWith(item);
    end;
    item.Free;
    av[0].VInt:=i;
    Player.StorageToMsgPlayer();
    exit;
  end;


  if(obj <> nil) and (item <> nil) then begin
    New(su);
    su.FPlace:=Obj;
    su.FSlot:=Player.StorageSlotFindEmpty(obj);
    su.FItem:=item;

    av[0].VInt:=Player.FStorage.Add(su);
    Player.StorageToMsgPlayer();
  end;
end;


procedure SF_GetItemFromStorage(av:array of TVarEC; code:TCodeEC);
var
  no: integer;
  su: PStorageUnit;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script GetItemFromStorage');
  no:=av[1].VInt;
  av[0].VDW:=0;

    if(no >= 0) and (no < Player.FStorage.Count) then begin
      su:=Player.FStorage.Items[no];
      Player.FStorage.Delete(no);
      Player.StorageToMsgPlayer();

      av[0].VDW:=Cardinal(su.FItem);
      Dispose(su);
    end;
end;

procedure SF_FindItemInStorage(av:array of TVarEC; code:TCodeEC);
var
  i:integer;
  item:TItem;
  su: PStorageUnit;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script FindItemInStorage');
  item:=TItem(av[1].VDW);
  av[0].VInt:=-1;

  for i:=0 to Player.FStorage.Count-1 do
  begin
    su:=Player.FStorage.Items[i];
    if su.FItem<>item then continue;
    av[0].VInt:=i;
    exit;
  end;

end;

procedure SF_PutItemInVault(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script PutItemInVault');
  Galaxy.StoreItem(av[1].VStr,TObject(av[2].VDW));
end;

procedure SF_GetItemFromVault(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script GetItemFromVault');
  av[0].VDW:=Cardinal(Galaxy.UnStoreItem(av[1].VStr));
end;


procedure SF_DropItemInSystem(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  obj:TObject;
  item: TItem;
  despos: TDxy;
  fpos: TPos;
  di: PDropItem;
begin
  if(High(av) < 6) then raise Exception.Create('Error.Script DropItemInSystem');
  star:=TStar(av[1].VDW);
  obj:=TObject(av[2].VDW);
  if obj is TScriptItem then item:=TScriptItem(obj).FItem else item:=TItem(obj);
  fpos.X:=av[3].VInt;
  fpos.Y:=av[4].VInt;
  despos.X:=av[5].VFloat;
  despos.Y:=av[6].VFloat;
  av[0].VInt:=0;

  if(star <> nil) and (item <> nil) then begin
    item.FPos:=fpos;

    di:=AllocEC(sizeof(TDropItem));
    di.FItem:=item;
    di.FDes:=despos;
    di.FIdShip:=0;
    di.FInStar:=false;
    di.FUse:=false;

    av[0].VInt:=star.FItemsDrop.Add(di);
  end;
end;

procedure SF_StopMovingItem(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  obj:TObject;
  item: TItem;
  di: PDropItem;
  i:integer;
  lFilmObj: TEFilmObj;
  step:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script StopMovingItem');
  star:=TStar(av[1].VDW);
  obj:=TObject(av[2].VDW);
  if obj is TScriptItem then item:=TScriptItem(obj).FItem else item:=TItem(obj);
  av[0].VInt:=0;

  for i:=0 to star.FItemsDrop.Count-1 do
  begin
    di:=star.FItemsDrop.Items[i];
    if di.FItem<>item then continue;
    di.FItem:=nil;
    star.FItemsDrop.Delete(i);
    FreeEC(di);
    star.FItems.Add(item);
    if star.FFilmBuild then
    begin
      step:=star.FCurStep;

      item.FFilmObj := GFilm.ObjAdd(item.FId, item.GraphItem, '', '');
      GFilm.OrderMove(step, item.FFilmObj, item.FPos);
      GFilm.OrderGraphConnect(step, item.FFilmObj);
    end;

    av[0].VInt:=1;
    exit;
  end;
end;

procedure SF_StarItems(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  no: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script StarItems');
  star:=TStar(av[1].VDW);
  if(star <> nil) then
  begin
    if(High(av) = 1) then
    begin
      av[0].VInt:=star.FItems.Count;
    end else begin
      no:=av[2].VInt;
      if(no >= 0) and (no < star.FItems.Count) then av[0].VDW:=Cardinal(star.FItems.Items[no]) else av[0].VDW:=0;
    end;
  end else av[0].VInt:=0;
end;


procedure SF_GetItemFromStar(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  item: TItem;
  no: integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script GetItemFromStar');
  star:=TStar(av[1].VDW);
  av[0].VDW:=0;
  if star = nil then exit;

  if (av[2].VType = vtDW) and (av[2].VDW > 65536) then
  begin
    item:=TItem(av[2].VDW);
    no:=star.FItems.IndexOf(item);
    if no<0 then exit;
  end else begin
    no:=av[2].VInt;
    if(no < 0) or (no >= star.FItems.Count) then exit;
    item:=star.FItems[no];
  end;

  if not star.FFilmBuild then item.DeleteContainer
  else if item.FGraphItem<>nil then
  begin
    GFilm.OrderGraphDisconnect(star.FCurStep, item.FFilmObj);
    //GFilm.OrderDestroy(star.FCurStep, item.FFilmObj);
    star.FDestroyObjEndFilm.Add(item.FFilmObj);
    DetachFromSE(TObjectSE(item.FGraphItem));
  end;

  star.FItems.Delete(no);
  star.DelTargetItem(item);

  av[0].VDW:=Cardinal(item);

end;

procedure SF_PlanetItems(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  no,cnt: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetItems');
  planet:=TPlanet(av[1].VDW);

  if(planet <> nil) then
  begin
    if planet.FGoneItems<>nil then cnt:=planet.FGoneItems.Count else cnt:=0;

    if(High(av) = 1) then
    begin
      av[0].VInt:=cnt;
    end else begin
      no:=av[2].VInt;
      if(no >= 0) and (no < cnt) then av[0].VDW:=Cardinal(PGoneItem(planet.FGoneItems.Items[no]).FItem) else av[0].VDW:=0;
    end;
  end else av[0].VDW:=0;
end;


procedure SF_StorageItems(av:array of TVarEC; code:TCodeEC);
var
  no: integer;
begin
  if(High(av) < 1) then begin
    av[0].VInt:=Player.FStorage.Count;
  end else begin
    no:=av[1].VInt;
    if(no >= 0) and (no < Player.FStorage.Count) then av[0].VDW:=Cardinal(PStorageUnit(Player.FStorage.Items[no]).FItem) else av[0].VDW:=0;
  end;
end;


procedure SF_StorageItemLocation(av:array of TVarEC; code:TCodeEC);
var
  no: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script StorageItemLocation');
  no:=av[1].VInt;
  av[0].VDW:=0;
  if(no >= 0) and (no < Player.FStorage.Count) then av[0].VDW:=Cardinal(PStorageUnit(Player.FStorage.Items[no]).FPlace);
end;


procedure SF_ShopItems(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  no: integer;
  i,cnt: integer;
  eqShop:TObjectList;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShopItems');
  obj:=TObject(av[1].VDW);

  if obj = nil then raise Exception.Create('Error.Script ShopItems shop=nil');

  if obj is TPlanet then eqShop:=TPlanet(obj).FEquipmentShop
  else if obj is TRuins then eqShop:=TRuins(obj).FEquipmentShop
  else raise Exception.Create('Error.Script ShopItems obj not a shop');


    if(High(av) = 1) then
    begin
      cnt:=0;

      if(GShopList <> nil) and ((Player.FCurPlanet = obj) or (Player.FCurShip = obj)) then
      begin
        for i:=0 to GShopList.Count-1 do
        begin
          if(GShopList.Items[i] = nil) then continue;
          if(TShopSlot(GShopList.Items[i]).FEq = nil) then continue;
          inc(cnt);
        end;
      end else begin
        for i:=0 to eqShop.Count-1 do if eqShop.Items[i] <> nil then inc(cnt);
      end;

      av[0].VInt:=cnt;

    end else begin

      no:=av[2].VInt;
      av[0].VDW:=0;
      if(GShopList <> nil) and ((Player.FCurPlanet = obj) or (Player.FCurShip = obj)) then
      begin
        //if(no >= 0) and (no < GShopList.Count) then av[0].VDW:=Cardinal(TShopSlot(GShopList.Items[no]).FEq);
        cnt:=-1;
        for i:=0 to GShopList.Count-1 do
        begin
          if(GShopList.Items[i] = nil) then continue;
          if(TShopSlot(GShopList.Items[i]).FEq = nil) then continue;
          inc(cnt);
          if cnt=no then
          begin
            av[0].VDW:=Cardinal(TShopSlot(GShopList.Items[i]).FEq);
            break;
          end;

        end;

        for i:=0 to GShopList.Count-1 do
        begin
          if(GShopList.Items[i] = nil) then continue;
          if(TShopSlot(GShopList.Items[i]).FEq = nil) then continue;
          inc(cnt);
        end;

      end else begin
        if(no >= 0) and (no < eqShop.Count) then av[0].VDW:=Cardinal(eqShop.Items[no]);
      end;
      
    end;

end;


procedure SF_AddDialogOverride(av:array of TVarEC; code:TCodeEC);
var
  dlgovd: PDialogOverride;
  tstr:WideString;
  no:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script AddDialogOverride');

  tstr:=av[1].VStr;
  if GetCountParEC(tstr,':')>1 then
  begin
    no:=FindScriptTempl(GetStrParEC(tstr,0,':'));
    if no<0 then exit;
    no:=TScriptTemplUnit(GScriptTempl.Items[no]).FRunScript;
    if no<0 then exit;
    New(dlgovd);
    dlgovd.FScript:=Galaxy.FScripts[no];
    dlgovd.FDialog:=GetStrParEC(tstr,1,':');

  end else begin
    New(dlgovd);
    dlgovd.FScript:=GScriptCur;
    dlgovd.FDialog:=tstr;
  end;

  dlgovd.FPriority:=av[2].VInt;

  if High(av) > 2 then dlgovd.FData:=av[3].VDW else dlgovd.FData:=0;

  if(DialogOverrideList = nil) then DialogOverrideList:=TObjectList.Create();
  DialogOverrideList.Add(dlgovd);
end;

procedure SF_AddDialogInject(av:array of TVarEC; code:TCodeEC);
var
  di: PDialogInject;
  tstr:WideString;
  no:integer;
begin
  if High(av) < 4 then raise Exception.Create('Error.Script AddDialogInject');

  tstr:=av[1].VStr;
  if GetCountParEC(tstr,':')>1 then
  begin
    no:=FindScriptTempl(GetStrParEC(tstr,0,':'));
    if no<0 then exit;
    no:=TScriptTemplUnit(GScriptTempl.Items[no]).FRunScript;
    if no<0 then exit;
    New(di);
    di.FScript:=Galaxy.FScripts[no];
    di.FDialog:=GetStrParEC(tstr,1,':');

  end else begin
    New(di);
    di.FScript:=GScriptCur;
    di.FDialog:=tstr;
  end;

  di.FText:=av[2].VStr;
  di.FAnswer:=av[3].VStr;
  di.FPriority:=av[4].VInt;

  if High(av) > 4 then di.FReplace:=(av[5].VInt <> 0) else di.FReplace:=false;
  if High(av) > 5 then di.FData:=av[6].VDW else di.FData:=0;

  if High(av) > 6 then
  begin
    di.FCodeOnSelect:=av[7].VStr;
    di.FCodeScript:=GScriptCur;
  end else begin
    di.FCodeOnSelect:='';
    di.FCodeScript:=nil;
  end;

  if(DialogInjectList = nil) then DialogInjectList:=TObjectList.Create();
  DialogInjectList.Add(di);
end;

procedure SF_InjectAnswer(av:array of TVarEC; code:TCodeEC);
var
  tstr,tstr2:WideString;
  cnt,no:integer;
  di: PDialogInject;
begin
  if High(av) < 3 then raise Exception.Create('Error.Script InjectAnswer');

  tstr:=av[1].VStr;
  if GetCountParEC(tstr,':')>1 then
  begin
    no:=FindScriptTempl(GetStrParEC(tstr,0,':'));
    if no<0 then exit;
    no:=TScriptTemplUnit(GScriptTempl.Items[no]).FRunScript;
    if no<0 then exit;
    New(di);
    di.FScript:=Galaxy.FScripts[no];
    di.FDialog:=GetStrParEC(tstr,1,':');

  end else begin
    New(di);
    di.FScript:=GScriptCur;
    di.FDialog:=tstr;
  end;

  di.FText:='';
  di.FAnswer:=av[2].VStr;
  di.FPriority:=0;
  di.FData:=av[3].VDW;
  di.FReplace:=false;

  if High(av) > 3 then
  begin
    di.FCodeOnSelect:=av[4].VStr;
    di.FCodeScript:=GScriptCur;
  end else begin
    di.FCodeOnSelect:='';
    di.FCodeScript:=nil;
  end;

  if(DialogInjectList = nil) then DialogInjectList:=TObjectList.Create();
  DialogInjectList.Add(di);

  tstr:=di.FAnswer; tstr2:='';
  cnt:=GetCountParEC(tstr,'~');
  if cnt>1 then
  begin
    tstr2:=GetStrParEC(tstr,0,'~');
    tstr:=GetStrParEC(tstr,1,cnt-1,'~');
  end;

  if Player.InShip then
  begin
    if tstr2='block' then GFormRuinsTalk.A_Add(tstr, g_TalkEmpty, 0)
    else GFormRuinsTalk.A_Add(di.FAnswer, GFormRuinsTalk.I_DialogScriptContinue, Cardinal(di));
  end
  else if Player.InPlanet then
  begin
    if tstr2='block' then GFormGov.A_Add(tstr, g_TalkEmpty, 0)
    else GFormGov.A_Add(di.FAnswer, GFormGov.I_DialogScriptContinue, Cardinal(di));
  end
  else begin
    if tstr2='block' then GFormTalk.A_Add(tstr, g_TalkEmpty, 0)
    else if tstr2='snap' then GFormTalk.A_Add(tstr, GFormTalk.I_DialogScriptContinue, Cardinal(di))
    else GFormTalk.A_Add(di.FAnswer, GFormTalk.I_DialogScriptContinue, Cardinal(di));
  end;
  //GAnswerData var will have data of chosen answer
end;

procedure SF_AddDialogBlock(av:array of TVarEC; code:TCodeEC);
var
  di: PDialogBlock;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script AddDialogBlock');

  New(di);
  di.FAnswer:=av[1].VStr;
  if(High(av) > 1) then di.FBlockType:=byte(av[2].VInt)
  else di.FBlockType:=2;//0 - normal, 1 - grey unselectable, >=2 - delete

  if(DialogBlockList = nil) then DialogBlockList:=TObjectList.Create();
  DialogBlockList.Add(di);
end;

procedure SF_GotoGov(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=Player.FGotoGov;
  //if(High(av) < 1) then raise Exception.Create('Error.Script GotoGov');

  if High(av) >= 1 then Player.FGotoGov:=av[1].VInt;
end;

procedure SF_GetShipPlanet(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script GetShipPlanet');
  ship:=TShip(av[1].VDW);
  if ship=Player.FBridge then av[0].VDW:=Cardinal(Player.FBridgeCurPlanet)
  else av[0].VDW:=Cardinal(ship.FCurPlanet);
end;

procedure SF_GetShipHomePlanet(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script GetShipHomePlanet');
  ship:=TShip(av[1].VDW);
  av[0].VDW:=Cardinal(ship.FHomePlanet);
end;

procedure SF_GetShipRuins(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script GetShipRuins');
  ship:=TShip(av[1].VDW);
  if ship=Player.FBridge then av[0].VDW:=Cardinal(Player.FBridgeCurShip)
  else av[0].VDW:=Cardinal(ship.FCurShip);
end;

procedure SF_GetTalkShip(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VDW:=Cardinal(GTalk_FShip);
end;

procedure SF_TalkByAI(av:array of TVarEC; code:TCodeEC);
begin
  if GTalk_FComputer then av[0].VInt:=1 else av[0].VInt:=0;
end;

procedure SF_GetTalkType(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=integer(GTalk_FTalkType);
end;


procedure SF_ScriptRun(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  planet: TPlanet;
  str: WideString;
  i: integer;
  script: TScript;
begin
  if(High(av) < 3) then raise Exception.Create('Error.Script ScriptRun');
  star:=TStar(av[1].VDW);
  planet:=TPlanet(av[2].VDW);
  str:=av[3].VStr;
  av[0].VInt:=0;

  for i:=0 to Galaxy.FScripts.Count-1 do
  begin
    script:=TScript(Galaxy.FScripts.Items[i]);
    if script.FCD = str then
    begin
      if script.FShips.Count > 0 then exit;
      if ScriptReCreate(script, star, planet) then av[0].VInt:=1;
      exit;
    end;
  end;

  if ScriptCreateByName(star, planet, str) then av[0].VInt:=1;

end;


procedure SF_SFT(av:array of TVarEC; code:TCodeEC);
var
  i: integer;

  procedure SFTarray(preStr:WideString; v:TVarEC);
  var j:integer;
      v2:TVarEC;
      tstr:WideString;
  begin
    for j:=0 to v.VArray.Count-1 do
    begin
      v2:=v.VArray.Items[j];
      if v2.Name<>'' then tstr:=preStr+v2.Name else tstr:=preStr+inttostrEC(j);
      if v2.VType<>vtArray then SFT(tstr+']='+v2.VStr) else SFTarray( tstr+',',v2);
    end;
  end;
begin
  if(High(av) < 1) then exit;

  for i:=1 to High(av) do
  begin
    if av[i].VType = vtArray then SFTarray(av[i].Name+'[',av[i])
    else SFT(av[i].VStr);
  end;
end;


procedure SF_StartTextQuest(av:array of TVarEC; code:TCodeEC);
var req:PScriptTQRequest;
begin
  if (High(av) = 0) then begin av[0].VInt:=GScriptsThatCalledTQ.Count; exit; end;
  
  //if GScriptQuestFlag then begin av[0].VInt:=0; exit; end;
  //if(High(av) < 1) then raise Exception.Create('Error.Script StartTextQuest');

  //GScriptQuestFlag:=true;
  //GScriptQuestName:=av[1].VStr;


  new(req);
  req.FQuestName:=av[1].VStr;
  if(High(av) > 1) then req.FQuestWinAction:=av[2].VStr else req.FQuestWinAction:='';
  if(High(av) > 2) then req.FQuestLossAction:=av[3].VStr else req.FQuestLossAction:='';
  req.FScript:=GScriptCur;

  GScriptsThatCalledTQ.Add(req);

  if GScriptCur<>nil then GScriptCur.FCodeInit.LocalVar.GetVar('GQuestStatus').VInt:=1;
  //GScriptQuestRun:=true;
  //GScriptThread.MakeRun();

  av[0].VInt:=1;
end;


procedure SF_CreateABShip(av:array of TVarEC; code:TCodeEC);
var
  i: integer;
  shipab: TabShipAI;
  obj:TObject;
begin
  // 1 - SE_name, 2 - isfriend, 3 - hp %, 4 - power %
  if(High(av) < 1) then raise Exception.Create('Error.Script CreateABShip');

  if GScriptCur<>GLastScriptThatCreatedABShip then
  begin
    GABShipsForScriptAB.Clear;
    //GScriptABPlayerDamage:=100;
  end;
  GLastScriptThatCreatedABShip:=GScriptCur;

  shipab:=TabShipAI.Create;
  shipab.FShipType:=av[1].VStr;
  shipab.FNoRandomDrop:=true;
  if High(av) > 1 then shipab.FSide:=av[2].VInt else shipab.FSide:=0;

  if(High(av) > 2) then shipab.FPercentHitPoints:=av[3].VInt else shipab.FPercentHitPoints:=100;
  if(High(av) > 3) then shipab.FPercentPower:=av[4].VInt else shipab.FPercentPower:=100;
  if(High(av) > 4) then shipab.FShipLabel:=av[5].VStr else shipab.FShipLabel:='';
  if(High(av) > 5) then
  begin
    obj:=TObject(av[6].VDW);
    if av[6].VInt = -1 then shipab.FNoRandomDrop:=false
    else if obj is TScriptItem then shipab.FCustomDrop:=TScriptItem(obj).FItem
    else shipab.FCustomDrop:=TItem(obj);
  end else shipab.FCustomDrop:=nil;

  // ????????? ??????? ? ??????
  GABShipsForScriptAB.Add(shipab);
  av[0].VDW:=Cardinal(shipab);
end;



procedure SF_ConvertToABShip(av:array of TVarEC; code:TCodeEC);
var
  i: integer;
  ship: TShip;
  shipab: TabShipAI;
  w: TWeapon;
  obj:TObject;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ConvertToABShip');

  if GScriptCur<>GLastScriptThatCreatedABShip then
  begin
    GABShipsForScriptAB.Clear;
    //GScriptABPlayerDamage:=100;
  end;
  GLastScriptThatCreatedABShip:=GScriptCur;

  ship:=TShip(av[1].VDW);
  if(ship <> nil) then
  begin
    shipab:=TabShipAI.Create;
    shipab.FNoRandomDrop:=true;

    //if(ship is TRuins) then shipab.InitAnim(ship.FGraphShip.TypeO, max(ship.FGraphShip.Size.X, ship.FGraphShip.Size.Y))
    //else shipab.Init(ship.FGraphShip.TypeO, ship.FGraphShip.Size.X);

    if ship.FGraphShip is TRuinsSE then shipab.InitAnim(ship.FGraphShip.TypeO, max(ship.FGraphShip.Size.X, ship.FGraphShip.Size.Y))
    else shipab.Init(ship.FGraphShip.TypeO, ship.FGraphShip.Size.X);

    shipab.FIsConvFromShip:=true;
    shipab.FHitPointsMax:=ship.FHull.FSize;
    shipab.FHitPoints:=ship.FHull.FHitPoints;

    shipab.FWeaponCnt:=0;

    ship.SlotCorrect;
    for i:=0 to 4 do
    begin
      w:=ship.SlotGetEquipment(t_Weapon1, i) as TWeapon;
      if not ship.AbleToUse(w) then continue;

      if w.FItemType<>t_CustomWeapon then abWaeponInitStd(@(shipab.FWeapon[i]), w.FItemType)
      else abWaeponInitStd(@(shipab.FWeapon[i]), w.WeaponInfo.ABWeaponType);
      shipab.FWeapon[i].FSlot:=w.FSlot;

      shipab.FWeaponCnt:=shipab.FWeaponCnt+1;
    end;
    shipab.FWeaponCur:=0;

    if High(av) > 1 then shipab.FSide:=av[2].VInt else shipab.FSide:=0;

    if(High(av) > 2) then shipab.FPercentHitPoints:=av[3].VInt else shipab.FPercentHitPoints:=100;
    if(High(av) > 3) then shipab.FPercentPower:=av[4].VInt else shipab.FPercentPower:=100;
    if(High(av) > 4) then shipab.FShipLabel:=av[5].VStr else shipab.FShipLabel:='';
    if(High(av) > 5) then
    begin
      obj:=TObject(av[6].VDW);
      if av[6].VInt = -1 then shipab.FNoRandomDrop:=false
      else if obj is TScriptItem then shipab.FCustomDrop:=TScriptItem(obj).FItem
      else shipab.FCustomDrop:=TItem(obj);
    end else shipab.FCustomDrop:=nil;

    GABShipsForScriptAB.Add(shipab);
    av[0].VDW:=Cardinal(shipab);
  end;
end;

procedure SF_ABShipModifiers(av:array of TVarEC; code:TCodeEC);
var shipab: TabShip;
    k:^single;
    str:WideString;
begin
  if (High(av) < 2) then raise Exception.Create('Error.Script PlayerABDamageMod');

  if TObject(av[1].VDW) = Player then shipab:=ab_player
  else shipab:=TabShipAI(av[1].VDW);//abship from event t_OnStartAB or from functions CreateABShip and ConvertToABShip

  if shipab=nil then
  begin
    av[0].VInt:=0;
    exit;
  end;

  str:=LowerCase(av[2].VStr);

  if str='damage' then k:=@(shipab.FkDamage)
  else if str='recharge' then k:=@(shipab.FkRecharge)
  else if str='speed' then k:=@(shipab.FkSpeed)
  else if str='gravity' then k:=@(shipab.FkGravity)
  else if str='regen' then k:=@(shipab.FkRegen)
  else if str='fragility' then k:=@(shipab.FkDamageTake)
  else if str='luck' then k:=@(shipab.FkLuckForDrops)
  else exit;

  av[0].VInt:=Round(100*k^);
  if (High(av) > 2) then k^:=av[3].VInt*0.01;

end;

procedure SF_StartAB(av:array of TVarEC; code:TCodeEC);
var req:PScriptABRequest;
begin
  if (High(av) = 0) then begin av[0].VInt:=GScriptsThatCalledAB.Count; exit; end;

  //if GScriptABFlag then begin av[0].VInt:=0; exit; end;
  //if(High(av) < 1) then raise Exception.Create('Error.Script StartAB');

  if GScriptCur<>GLastScriptThatCreatedABShip then
  begin
    GABShipsForScriptAB.Clear;
    //GScriptABPlayerDamage:=100;
  end;
  GLastScriptThatCreatedABShip:=GScriptCur;

  new(req);

  //GScriptABFlag:=true;
  req.FABMapName:=av[1].VStr;

  req.FABbg:=0;
  req.FABbg_str:='';
  //req.FABPlayerDamage:=GScriptABPlayerDamage;
  //GScriptABPlayerDamage:=100;
  req.FScript:=GScriptCur;
  req.FABShips:=TObjectList.Create;
  while GABShipsForScriptAB.Count>0 do
  begin
    req.FABShips.Add(GABShipsForScriptAB.Items[0]);
    GABShipsForScriptAB.Delete(0);
  end;

  if(High(av) > 1) then
  begin
    if(av[2].VType = vtInt) then req.FABbg:=av[2].VInt
    else if(av[2].VType = vtStr) then req.FABbg_str:=av[2].VStr;
  end;

  GScriptsThatCalledAB.Add(req);

  if GScriptCur<>nil then GScriptCur.FCodeInit.LocalVar.GetVar('GABStatus').VInt:=1;

  av[0].VInt:=1;
end;


procedure SF_StartRobots(av:array of TVarEC; code:TCodeEC);
var req:PScriptPBRequest;
  robotresult: integer;
  tmap,tstart,twin,tloss,tplace: WideString;
  curform: mlForm;
begin
  if (High(av) = 0) then begin av[0].VInt:=GScriptsThatCalledPB.Count; exit; end;

  if(High(av) < 5) then raise Exception.Create('Error.Script StartRobots');

  new(req);

  req.FRobotMap:=av[1].VStr;
  req.FRobotStart:=av[2].VStr;
  req.FRobotWin:=av[3].VStr;
  req.FRobotLoss:=av[4].VStr;
  req.FRobotPlace:=av[5].VStr;
  if(High(av) > 5) then req.FRobotStart:=av[6].VStr + req.FRobotStart else req.FRobotStart:='621' + req.FRobotStart;

  req.FScript:=GScriptCur;

  GScriptsThatCalledPB.Add(req);

  if GScriptCur<>nil then GScriptCur.FCodeInit.LocalVar.GetVar('GRobotStatus').VInt:=1;
end;

procedure SF_MarkRobotsMapAsUsed(av:array of TVarEC; code:TCodeEC);
var i:integer;
    mapName:WideString;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script MarkRobotsMapAsUsed');
  mapName:=av[1].VStr;

  for i:=0 to High(GRobotsMap) do
  begin
    if GRobotsMap[i].FFileName = mapName then
    begin
      SetLength(Player.FRobotMap,High(Player.FRobotMap)+2);
      with Player.FRobotMap[High(Player.FRobotMap)] do
      begin
        FId:=GRobotsMap[i].FId;
        FTime:=0;
        FBuildRobot:=0;
        FKillRobot:=0;
        FBuildTurret:=0;
        FKillTurret:=0;
        FKillBuilding:=0;
        FBonus:=1;
        FState:=0;
        FTurn:=Galaxy.FTurn;
      end;
      if (High(av)>1) and (av[2].VInt<>0) then Player.FLastPlanetBattleDate:=Galaxy.FTurn;
    end;
  end;

  raise Exception.Create('Error.Script MarkRobotsMapAsUsed map not found '+mapName);

end;



procedure SF_ShipOwner(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipOwner');
  ship:=TShip(av[1].VDW);
  if(ship <> nil) then
  begin
    av[0].VInt:=integer(ship.FOwner);
    if(High(av) > 1) then ship.FOwner:=TOwner(av[2].VInt);
  end else av[0].VInt:=-1;
end;

procedure SF_ShipPilotRace(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipPilotRace');
  ship:=TShip(av[1].VDW);
  if (ship <> nil) then
  begin
    av[0].VInt:=integer(ship.FPilotRace);
    if(High(av) > 1) then ship.FPilotRace:=TRace(av[2].VInt);
  end else av[0].VInt:=-1;
end;


procedure SF_ShipSkill(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
  skill, value:integer;
  totalVal:boolean;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ShipSkill');
  ship:=TShip(av[1].VDW);
  if ship = nil then exit;

  totalVal:=false;

  if av[2].VType = vtStr then
  begin
    if      av[2].VStr = 'Accuracy' then skill:=0
    else if av[2].VStr = 'AccuracyCur' then begin skill:=0; totalVal:=true; end
    else if av[2].VStr = 'Mobility' then skill:=1
    else if av[2].VStr = 'MobilityCur' then begin skill:=1; totalVal:=true; end
    else if av[2].VStr = 'Technical' then skill:=2
    else if av[2].VStr = 'TechnicalCur' then begin skill:=2; totalVal:=true; end
    else if av[2].VStr = 'Trader' then skill:=3
    else if av[2].VStr = 'TraderCur' then begin skill:=3; totalVal:=true; end
    else if av[2].VStr = 'Charm' then skill:=4
    else if av[2].VStr = 'CharmCur' then begin skill:=4; totalVal:=true; end
    else if av[2].VStr = 'Leadership' then skill:=5
    else if av[2].VStr = 'LeadershipCur' then begin skill:=5; totalVal:=true; end
    else raise Exception.Create('Error.Script ShipSkill unknown query '+av[2].VStr);
  end else begin
    skill:=av[2].VInt;
    if (skill < 0) or (skill > 5) then raise Exception.Create('Error.Script ShipSkill - invalid skill index');
  end;

  if totalVal then av[0].VInt:=ship.SkillCur(TSkills(skill))
  else av[0].VInt:=ship.FmSkills[TSkills(skill)];

  if(High(av) > 2) then
  begin
    value:=av[3].VInt;
    //if(value >= 0) and (value <= SkillsCnt) then ship.FmSkills[TSkills(skill)]:=value;
    ship.FmSkills[TSkills(skill)]:=max(0,min(SkillsCnt,value));
  end;
end;

procedure SF_ShipFace(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipFace');
  ship:=TShip(av[1].VDW);
  if(ship <> nil) then begin

    if(High(av) > 1) then
    begin
      if (av[2].VType=vtStr) then
      begin
        if (av[2].VStr='Init') then begin if ship.FFace=-1 then ship.Face; av[0].VInt:=ship.FFace; end
        else if (av[2].VStr='New') then begin ship.FFace:=-1; ship.Face; av[0].VInt:=ship.FFace; end
        else if (av[2].VStr='Path') then av[0].VStr:=ship.Face
        else raise Exception.Create('Error.Script ShipFace unknown keyword - '+av[2].VStr);
      end
      else
      begin
        av[0].VInt:=ship.FFace;
        ship.FFace:=av[2].VInt;
      end;
    end
    else av[0].VInt:=ship.FFace;
  end;
end;

procedure SF_ShipFreeExp(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipFreeExp');
  ship:=TShip(av[1].VDW);
  if(ship <> nil) then begin
    av[0].VInt:=ship.FFreePoints;
    if(High(av) > 1) then ship.FFreePoints:=av[2].VInt;
  end;
end;

procedure SF_GetShipExpByType(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script GetShipExpByType');
  ship:=TShip(av[1].VDW);
  if(ship <> nil) then
  begin
    if (High(av) = 1) or (ship<>Player) then av[0].VInt:=ship.FPoints else
    begin
      case av[2].VInt of
        1: av[0].VInt:=Player.FExpPointsForDominatorKills;
        2: av[0].VInt:=Player.FExpPointsForPirateKills;
        3: av[0].VInt:=Player.FExpPointsForGoodShipKills;
        4: av[0].VInt:=Player.FExpPointsForTrade;
        5: av[0].VInt:=Player.FPoints
                       - Player.FExpPointsForDominatorKills
                       - Player.FExpPointsForPirateKills
                       - Player.FExpPointsForGoodShipKills
                       - Player.FExpPointsForTrade;
        else av[0].VInt:=ship.FPoints;
      end;
    end;
  end;
end;




procedure SF_CoordX(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  pos: TPos;
  pol:TPolar;
begin
  if High(av)<1 then raise Exception.Create('Error.Script CoordX');
  obj:=TObject(av[1].VDW);
  av[0].VInt:=0;
  if(obj <> nil) then begin
    if(obj is TShip) then pos:=(obj as TShip).FPos
    else if(obj is TItem) then pos:=(obj as TItem).FPos
    else if(obj is TScriptItem) then
    begin
      if((obj as TScriptItem).FItem <> nil) then pos:=(obj as TScriptItem).FItem.FPos
      else raise Exception.Create('Error.Script CoordX - script item does not exist');
    end else if(obj is TScriptPlace) then pos:=(obj as TScriptPlace).GetCenter
    else if(obj is TPlanet) then pos:=(obj as TPlanet).CartesianPos
    else if(obj is TStar) then pos:=(obj as TStar).FPos
    else if(obj is TAsteroid) then pos:=(obj as TAsteroid).FPos
    else if(obj is TMissile) then pos:=(obj as TMissile).FPos
    else raise Exception.Create('Error.Script CoordX - Object type not supported');

    av[0].VInt:=Round(pos.X);
    if High(av)>1 then
    begin
      pos.X:=av[2].VInt;
      if(obj is TShip) then (obj as TShip).FPos:=pos
      else if(obj is TItem) then (obj as TItem).FPos:=pos
      else if(obj is TScriptItem) then (obj as TScriptItem).FItem.FPos:=pos
      else if(obj is TScriptPlace) then
      begin
        pol:=CartesianToPolar(Point( round(pos.X),round(pos.Y) ));
        (obj as TScriptPlace).FRadius:=round(pol.Radius);
        (obj as TScriptPlace).FAngle:=pol.Angle;
      end
      else if(obj is TPlanet) then
      begin
        (obj as TPlanet).FPolarPos:=CartesianToPolar(Point( round(pos.X),round(pos.Y) ));
        (obj as TPlanet).FGraphPlanet.Pos:=pos;
      end
      else if(obj is TStar) then (obj as TStar).FPos:=pos
      else if(obj is TAsteroid) then (obj as TAsteroid).FPos:=pos
      else if(obj is TMissile) then (obj as TMissile).FPos:=pos;
    end;
  end;
end;

procedure SF_CoordY(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  pos: TPos;
  pol:TPolar;
begin
  if High(av)<1 then raise Exception.Create('Error.Script CoordY');
  obj:=TObject(av[1].VDW);
  av[0].VInt:=0;
  if(obj <> nil) then begin
    if(obj is TShip) then pos:=(obj as TShip).FPos
    else if(obj is TItem) then pos:=(obj as TItem).FPos
    else if(obj is TScriptItem) then
    begin
      if((obj as TScriptItem).FItem <> nil) then pos:=(obj as TScriptItem).FItem.FPos
      else raise Exception.Create('Error.Script CoordY - script item does not exist');
    end else if(obj is TScriptPlace) then pos:=(obj as TScriptPlace).GetCenter
    else if(obj is TPlanet) then pos:=(obj as TPlanet).CartesianPos
    else if(obj is TStar) then pos:=(obj as TStar).FPos
    else if(obj is TAsteroid) then pos:=(obj as TAsteroid).FPos
    else if(obj is TMissile) then pos:=(obj as TMissile).FPos
    else raise Exception.Create('Error.Script CoordY - Object type not supported');

    av[0].VInt:=Round(pos.Y);
    if High(av)>1 then
    begin
      pos.Y:=av[2].VInt;
      if(obj is TShip) then (obj as TShip).FPos:=pos
      else if(obj is TItem) then (obj as TItem).FPos:=pos
      else if(obj is TScriptItem) then (obj as TScriptItem).FItem.FPos:=pos
      else if(obj is TScriptPlace) then
      begin
        pol:=CartesianToPolar(Point( round(pos.X),round(pos.Y) ));
        (obj as TScriptPlace).FRadius:=round(pol.Radius);
        (obj as TScriptPlace).FAngle:=pol.Angle;
      end
      else if(obj is TPlanet) then
      begin
        (obj as TPlanet).FPolarPos:=CartesianToPolar(Point( round(pos.X),round(pos.Y) ));
        (obj as TPlanet).FGraphPlanet.Pos:=pos;
      end
      else if(obj is TStar) then (obj as TStar).FPos:=pos
      else if(obj is TAsteroid) then (obj as TAsteroid).FPos:=pos
      else if(obj is TMissile) then (obj as TMissile).FPos:=pos;
    end;
  end;
end;


procedure SF_ShipSetCoords(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 3) then raise Exception.Create('Error.Script ShipSetCoords');
  ship:=TShip(av[1].VDW);
  if(ship <> nil) then
  begin
    ship.FPos.X:=av[2].VInt;
    ship.FPos.Y:=av[3].VInt;

    ship.FGraphShip.Pos := ship.FPos;

  end;
end;

procedure SF_ShipAngle(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipAngle');
  ship:=TShip(av[1].VDW);
  if(ship <> nil) then
  begin
    av[0].VFloat:=ship.FAngle;
    if(High(av) > 1) then
    begin
      ship.FAngle:=av[2].VFloat;
      ship.FGraphShip.Angle:=AngleGraTo256(ship.FAngle);
    end;
  end;
end;



procedure SF_ObjectType(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ObjectType');
  av[0].VInt:=0;
  obj:=TObject(av[1].VDW);
  if(obj is TStar) then av[0].VInt:=1
  else if(obj is THole) then av[0].VInt:=2
  else if(obj is TPlanet) then av[0].VInt:=3
  else if(obj is TRuins) then av[0].VInt:=4
  else if(obj is TShip) then av[0].VInt:=5
  else if(obj is TItem) then av[0].VInt:=6
  else if(obj is TMissile) then av[0].VInt:=7
  else if(obj is TAsteroid) then av[0].VInt:=8;
end;


procedure SF_ShipInHyperSpace(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) <> 1) then raise Exception.Create('Error.Script ShipInHyperSpace');
  av[0].VInt:=0;
  ship:=TShip(av[1].VDW);
  if(ship <> nil) then av[0].VInt:=Cardinal(ship.FInHiperSpace);
end;


procedure SF_ShipStatus(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  ship: TRanger;
  status: tStatus;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ShipStatus');
  obj:=TObject(av[1].VDW);

  if(obj is TRanger) then ship:=TRanger(obj)
  else raise Exception.Create('Error.Script ShipStatus - not Ranger');

  status:=tStatus(av[2].VInt); //Trader,Pirate,Warrior
  av[0].VInt:=integer(ship.FStatus[status]);
  if (High(av) > 2) then ship.FStatus[status]:=TPercent(av[3].VInt);
end;


procedure SF_BuyRanger(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  ship: TShip;
  monPerc:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script BuyRanger');
  monPerc:=100;
  if (High(av) > 1) then monPerc:=av[2].VInt;
  planet:=TPlanet(av[1].VDW);
  if(planet <> nil) then begin
    ship:=TShip(planet.BuyRanger(monPerc));
    av[0].VDW:=Cardinal(ship);
  end;
end;

procedure SF_BuyWarrior(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  ship: TShip;
  monPerc:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script BuyWarrior');
  monPerc:=100;
  if (High(av) > 1) then monPerc:=av[2].VInt;
  planet:=TPlanet(av[1].VDW);
  if(planet <> nil) then begin
    ship:=TShip(planet.BuyWarrior(monPerc));
    av[0].VDW:=Cardinal(ship);
  end;
end;

procedure SF_BuyBigWarrior(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  ship: TShip;
  monPerc:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script BuyBigWarrior');
  monPerc:=100;
  if (High(av) > 1) then monPerc:=av[2].VInt;
  planet:=TPlanet(av[1].VDW);
  if(planet <> nil) then begin
    ship:=TShip(planet.BuyBigWarrior(monPerc));
    av[0].VDW:=Cardinal(ship);
  end;
end;

procedure SF_BuyDomik(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script BuyDomik');
  planet:=TPlanet(av[1].VDW);
  if(planet <> nil) then begin
    //obsolete
    //ship:=TShip(planet.BuyRandomKlingNormal());
    ship:=TShip(planet.BuyRandomKling());
    av[0].VDW:=Cardinal(ship);
  end;
end;

procedure SF_BuyDomikExtremal(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script BuyDomikExtremal');
  planet:=TPlanet(av[1].VDW);
  if(planet <> nil) then
  begin
    if High(av)= 1 then ship:=TShip(planet.BuyRandomKling())
    else ship:=TShip(planet.BuyKling(TKlingType(av[2].VInt)));//0 - boss, 1-5 - ekventor-shtip, 6 - bertor, 7 - klig
    av[0].VDW:=Cardinal(ship);
  end;
end;

procedure SF_BuyTranclucator(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  ship: TShip;
  small:boolean;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script BuyTrank');
  planet:=TPlanet(av[1].VDW);
  if(planet <> nil) then
  begin
    small:=true;
    if High(av) > 1 then small:=(av[2].VInt<>0);//add 0 to buy stronger tranc
    ship:=TShip(planet.BuyTranclucator(small));
    av[0].VDW:=Cardinal(ship);
  end;
end;


procedure SF_TransferShip(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  star1,star2: TStar;
  planet: TPlanet;
  ruins: TRuins;
  ship: TShip;
  i: integer;
  lastobj: TObject;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script TransferShip');

  ship:=TShip(av[1].VDW);
  if(ship <> nil) then begin
    star1:=ship.FCurStar;
    if(star1 <> nil) then begin
      obj:=TObject(av[2].VDW);
      if(obj <> nil) then begin
        if(not (obj is TStar)) and (not (obj is TPlanet)) and (not (obj is TRuins)) then raise Exception.Create('Error.Script TransferShip - invalid destination');

        planet:=nil;
        ruins:=nil;
        if(obj is TPlanet) then begin
          planet:=TPlanet(obj);
          star2:=planet.FStar;
        end else if(obj is TRuins) then begin
          ruins:=TRuins(obj);
          star2:=ruins.FCurStar;
        end else star2:=TStar(obj);

        i:=star1.FShips.IndexOf(ship);
        if(i >= 0) and  (i < star1.FShips.Count) then star1.FShips.Delete(i);
        star2.FShips.Add(ship);
        ship.FCurStar:=star2;

        lastobj:=nil;
        if(ship.FCurPlanet <> nil) then begin
          if(ship is TNormalShip) then (ship as TNormalShip).FLastPlanet:=ship.FCurPlanet;
          lastobj:=ship.FCurPlanet;
        end else if(ship.FCurShip <> nil) then begin
          if(ship is TRanger) then (ship as TRanger).FLastShip:=ship.FCurShip;
          lastobj:=ship.FCurShip;
        end;

        if (ship = Player) and Player.InPlanetOrShip then
        begin
          ShopListToEquipmentShop;
          ShopListDestroy;
        end;

        ship.FCurPlanet:=planet;
        ship.FCurShip:=ruins;
        ship.FOrder:=TOrderType(0);
        ship.FOrderData:=0;
        ship.FOrderObj:=nil;
        ship.FOrderDes.X:=0;
        ship.FOrderDes.Y:=0;
        ship.FOrderAbsolut:=false;
        ship.FInHiperSpace:=false;

        if (ship = Player) and Player.InPlanetOrShip then
        begin
          EquipmentShopToShopList();
          GFormEquipmentShop.FreeImage();
          GFormEquipmentShop.BuildImage();
        end;
      end;
    end;
  end;
end;



procedure SF_OrderLock(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script OrderLock');

  ship:=TShip(av[1].VDW);
  if(ship <> nil) then begin
    av[0].VInt:=ship.FScriptOrderAbsolute;
    if(High(av) > 1) then ship.FScriptOrderAbsolute:=byte(av[2].VInt);
  end;
end;


procedure SF_OrderForsage(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script OrderForsage');
  ship:=TShip(av[1].VDW);
  av[0].VInt:=0;
  if (ship <> nil) {and (ship is TNormalShip)} then
  begin
    if {(ship as TNormalShip)}ship.FForsage then av[0].VInt:=1;
    if High(av)>1 then
     begin
       if (av[2].VInt<>0) then ship.FForsage := (ship.SlotCount(st_Forsage) > 0) and ship.AbleToUse(ship.FEngine)
       else ship.FForsage := false;
       ship.CalcParam;

       if (ship=Player) and (GetCurrentML = GFormStarMap) and (GFormStarMap.FMode = fsmm_Control) then
       begin
         GFormStarMap.ShipPathHide;
         Player.PathCalc(999999);
         GFormStarMap.ShipPathShow(ship);
       end;
     end;
  end;
end;

procedure SF_OrderNone(av:array of TVarEC; code:TCodeEC);
var
  scriptorder: byte;
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script OrderNone');

  ship:=TShip(av[1].VDW);
  if(ship <> nil) then
  begin
    scriptorder:=ship.FScriptOrderAbsolute;
    ship.FScriptOrderAbsolute:=0;
    ship.OrderNone();
    ship.FScriptOrderAbsolute:=scriptorder;

    if ship=Player then AutoBattleShip:=nil;

    if (ship=Player) and (GetCurrentML = GFormStarMap) and (GFormStarMap.FMode = fsmm_Control) then
    begin
      GFormStarMap.ShipPathHide;
      GFormStarMap.ShipPathShow(ship);
    end;
  end;
end;

procedure SF_OrderMove(av:array of TVarEC; code:TCodeEC);
var
  absolut: boolean;
  des: TDxy;
  scriptorder: byte;
  ship: TShip;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script OrderMove');
  ship:=TShip(av[1].VDW);
  if ship = nil then exit;

  scriptorder:=ship.FScriptOrderAbsolute;
  ship.FScriptOrderAbsolute:=0;

  if(High(av) > 2) then
  begin
    absolut:=false;
    if(High(av) > 3) then absolut:=(av[4].VInt <> 0);
    des.X:=av[2].VInt;
    des.Y:=av[3].VInt;
    ship.OrderMove(des, absolut);
  end
  else if (av[2].VType = vtDW) and (TObject(av[2].VDW) is TScriptPlace) then
  begin
    absolut:=false;
    if(High(av) > 2) then absolut:=(av[3].VInt <> 0);
    ship.OrderMove(TScriptPlace(av[2].VDW).GetPos((ship.FRnd+ship.FCurStar.FRnd)*Galaxy.FTurn), absolut);
  end
  else raise Exception.Create('Error.Script OrderMove invalid place');

  ship.FScriptOrderAbsolute:=scriptorder;

  if ship=Player then AutoBattleShip:=nil;

  if (ship=Player) and (GetCurrentML = GFormStarMap) and (GFormStarMap.FMode = fsmm_Control) then
  begin
    GFormStarMap.ShipPathHide;
    GFormStarMap.ShipPathShow(ship);
  end;
end;

procedure SF_OrderTeleport(av:array of TVarEC; code:TCodeEC);
var
  absolut: boolean;
  des: TDxy;
  scriptorder: byte;
  ship: TShip;
  duration:integer;
begin
  if(High(av) < 4) then raise Exception.Create('Error.Script OrderTeleport');
  absolut:=false;
  if(High(av) > 4) then absolut:=(av[5].VInt <> 0);
  des.X:=av[3].VInt;
  des.Y:=av[4].VInt;
  duration:=10;
  if(High(av) > 5) then duration:=av[6].VInt;

  if(av[1].VDW <> 0) and (av[2].VDW <> 0) then
  begin
    ship:=TShip(av[1].VDW);
    if(ship <> nil) then
    begin
      scriptorder:=ship.FScriptOrderAbsolute;
      ship.FScriptOrderAbsolute:=0;
      ship.OrderTeleport(TStar(av[2].VDW), des, duration, absolut);
      ship.FScriptOrderAbsolute:=scriptorder;

      if ship=Player then AutoBattleShip:=nil;

      if (ship=Player) and (GetCurrentML = GFormStarMap) and (GFormStarMap.FMode = fsmm_Control) then
      begin
        GFormStarMap.ShipPathHide;
        GFormStarMap.ShipPathShow(ship);
      end;
    end;
  end;
end;

procedure SF_OrderTakeOff(av:array of TVarEC; code:TCodeEC);
var
  scriptorder: byte;
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script OrderTakeOff');

  ship:=TShip(av[1].VDW);
  if(ship <> nil) then begin
    scriptorder:=ship.FScriptOrderAbsolute;
    ship.FScriptOrderAbsolute:=0;
    ship.OrderTakeOff();
    ship.FScriptOrderAbsolute:=scriptorder;
  end;
end;

procedure SF_OrderFollowShip(av:array of TVarEC; code:TCodeEC);
var
  absolut: boolean;
  ft: tFollowType;
  scriptorder: byte;
  ship: TShip;
begin
  if High(av)<2 then raise Exception.Create('Error.Script OrderFollowShip');

  absolut:=false;
  ft:=t_FollowNear;
  if(High(av) > 2) then ft:=tFollowType(av[3].VInt);
  if(High(av) > 3) then absolut:=(av[4].VInt <> 0);


  if(av[1].VDW <> 0) and (av[2].VDW <> 0) then begin
    ship:=TShip(av[1].VDW);
    if(ship <> nil) then
    begin
      scriptorder:=ship.FScriptOrderAbsolute;
      ship.FScriptOrderAbsolute:=0;
      ship.OrderFollowShip(TShip(av[2].VDW), ft, absolut);
      ship.FScriptOrderAbsolute:=scriptorder;

      if (ship=Player) and (GetCurrentML = GFormStarMap) and (GFormStarMap.FMode = fsmm_Control) then
      begin
        GFormStarMap.ShipPathHide;
        GFormStarMap.ShipPathShow(ship);
      end;
    end;
  end;
end;


procedure SF_OrderJumpHole(av:array of TVarEC; code:TCodeEC);
var
  absolut: boolean;
  ship: TShip;
  hole: THole;
  scriptorder: byte;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script OrderJumpHole');
  ship:=TShip(av[1].VDW);
  hole:=THole(av[2].VDW);
  if(ship <> nil) and (hole <> nil) then
  begin
    absolut:=false;
    if(High(av) > 2) then absolut:=(av[3].VInt <> 0);

    scriptorder:=ship.FScriptOrderAbsolute;
    ship.FScriptOrderAbsolute:=0;
    ship.OrderJumpHole(hole, absolut);
    ship.FScriptOrderAbsolute:=scriptorder;

    if ship=Player then AutoBattleShip:=nil;

    if (ship=Player) and (GetCurrentML = GFormStarMap) and (GFormStarMap.FMode = fsmm_Control) then
    begin
      GFormStarMap.ShipPathHide;
      GFormStarMap.ShipPathShow(ship);
    end;
  end;
end;


procedure SF_RelationToRanger(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  ship: TShip;
  relation: TPercent;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script RelationToRanger');
  av[0].VInt:=0;
  obj:=TObject(av[1].VDW);
  ship:=TShip(av[2].VDW);
  if(ship <> nil) then begin
    if(obj is TPlanet) then begin
      av[0].VInt:=integer(TPlanet(obj).FRelationToRangers.Items[Galaxy.FRangers.IndexOf(ship)]);

      if(High(av) > 2) then begin
        if av[3].VInt<0 then relation:=0
        else if av[3].VInt>100 then relation:=100
        else relation:=TPercent(av[3].VInt);
        TPlanet(obj).FRelationToRangers.Items[Galaxy.FRangers.IndexOf(ship)]:=pointer(relation);
      end;
    end else if(obj is TShip) then begin
      //av[0].VInt:=TShip(obj).RelationToShip(ship);
      if (TShip(obj).FRelationToRangers<>nil) and (TShip(obj).FRelationToRangers.Count>0) then
          av[0].VInt:=integer(TShip(obj).FRelationToRangers.Items[Galaxy.FRangers.IndexOf(ship)])
      else av[0].VInt:=TShip(obj).RelationToShip(ship);

      if(High(av) > 2) and (TShip(obj).FRelationToRangers<>nil) and (TShip(obj).FRelationToRangers.Count>0) then begin
        if av[3].VInt<0 then relation:=0
        else if av[3].VInt>100 then relation:=100
        else relation:=TPercent(av[3].VInt);
        TShip(obj).FRelationToRangers.Items[Galaxy.FRangers.IndexOf(ship)]:=pointer(relation);
      end;
    end;
  end;
end;


procedure SF_RelationToShip(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  ship: TShip;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script RelationToShip');
  av[0].VInt:=0;
  obj:=TObject(av[1].VDW);
  ship:=TShip(av[2].VDW);
  if(ship <> nil) then
  begin
    if(obj is TPlanet) then av[0].VInt:=TPlanet(obj).RelationToShip(ship)
    else if(obj is TShip) then av[0].VInt:=TShip(obj).RelationToShip(ship);
  end;
end;


procedure SF_StarOwner(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script StarOwner');
  star:=TStar(av[1].VDW);
  av[0].VInt:=0;
  if(star <> nil) then
  begin
    av[0].VInt:=integer(star.FStatus.Owners);
    if High(av) > 1 then star.FStatus.Owners:=TStarOwners(av[2].VInt);
  end;
end;

procedure SF_StarBattle(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script StarBattle');
  star:=TStar(av[1].VDW);
  av[0].VInt:=0;
  if(star <> nil) then av[0].VInt:=integer(star.FStatus.Battle);
end;

procedure SF_StarSeries(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script StarSeries');
  star:=TStar(av[1].VDW);
  av[0].VInt:=0;
  if(star <> nil) then begin
    av[0].VInt:=integer(star.FStatus.Series);
    if(High(av) > 1) then star.FStatus.Series:=TDominatorSeries(av[2].VInt);
  end;
end;


procedure SF_StarHoles(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  hole: THole;
  i,num,counter: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script StarSeries');
  star:=TStar(av[1].VDW);
  num:=-1;
  counter:=-1;
  av[0].VDW:=0;
  if(High(av) > 1) then num:=av[2].VInt;
  for i:=0 to Galaxy.FHoles.Count-1 do begin
    hole:=Galaxy.FHoles.Items[i];
    if(hole.FStar1 = star) or (hole.FStar2 = star) then begin
      counter:=counter + 1;
      if(counter = num) then begin
        av[0].VDW:=Cardinal(hole);
        exit;
      end;
    end;
  end;
  if(High(av) = 1) then av[0].VInt:=counter + 1;
end;



procedure SF_StarNearbyStars(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  no: integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script StarNearbyStars');
  av[0].VDW:=0;
  star:=TStar(av[1].VDW);
  if(star <> nil) then begin
    no:=av[2].VInt;
    if(no >= 0) and (no < Galaxy.FStars.Count) then av[0].VDW:=Cardinal(star.FStarDist[no].FStar);
  end;
end;


procedure SF_StarNearbyStarsDist(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  no: integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script StarNearbyStarsDist');
  av[0].VDW:=0;
  star:=TStar(av[1].VDW);
  if(star <> nil) then begin
    no:=av[2].VInt;
    if(no >= 0) and (no < Galaxy.FStars.Count) then av[0].VInt:=star.FStarDist[no].FDist;
  end;
end;

procedure SF_StarSetGraph(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script StarSetGraph');
  star:=TStar(av[1].VDW);
  DetachFromSE(TObjectSE(star.FGraphStar));
  LinkToSE(TObjectSE(star.FGraphStar) , ObjCreateSE('Star', av[2].VStr, Point(0, 0)));
  //example 'Star.01' (full path in main.dat Data.SE.Star.01)
  star.FGraphType := 'Process.Normal';
  star.FGraphStar.Pos := Dxy(0, 0);
end;


procedure SF_CreatePlanet(av:array of TVarEC; code:TCodeEC);
var
  i:integer;
  planet: TPlanet;
  star:TStar;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script CreatePlanet');
  star:=TStar(av[1].VDW);
  planet := TPlanet.Create;
  planet.ExtraGenericPlanetInit(star);
  Galaxy.FPlanets.Add(planet);
  av[0].VDW:=Cardinal(planet);

  if High(av) < 2 then star.FPlanets.Add(planet)
  else begin
    planet.FPolarPos.Radius:=av[2].VInt;
    if planet.FPolarPos.Radius>TPlanet(star.FPlanets.Last).FPolarPos.Radius then star.FPlanets.Add(planet)
    else for i:=0 to star.FPlanets.Count-1 do
    begin
      if planet.FPolarPos.Radius<TPlanet(star.FPlanets[i]).FPolarPos.Radius then
      begin
        star.FPlanets.Insert(i,planet);
        break;
      end;
    end;
  end;
end;


procedure SF_PlanetSetGraph(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  rot:word;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script PlanetSetGraph');
  planet:=TPlanet(av[1].VDW);

  if av[2].VType=vtStr then
  begin
    planet.FGraphName:=av[2].VStr;
    rot:=planet.FGraphPlanet.SpeedRotate;
    DetachFromSE(TObjectSE(planet.FGraphPlanet));
    LinkToSE(TObjectSE(planet.FGraphPlanet),ObjCreateSE('Planet', planet.FGraphName, Point(0, 0)));
    planet.FGraphPlanet.SpeedRotate:=rot;

  end else begin
    planet.FGraphNo := av[2].VInt; //number from Main.dat Data.SE.Planet
    DetachFromSE(TObjectSE(planet.FGraphPlanet));
    LinkToSE(TObjectSE(planet.FGraphPlanet),TPlanetSE.Create);
    GPlanetFC[planet.FGraphNo].FPlanet.CopyData(planet.FGraphPlanet);
    planet.FGraphName:=planet.FGraphPlanet.TypeO;
  end;
  planet.FGraphPlanet.Pos := PolarToCartesian(planet.FPolarPos);
  planet.FGraphRadius:=planet.FGraphPlanet.Radius;
end;

procedure SF_PlanetGetGraph(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetGetGraph');
  planet:=TPlanet(av[1].VDW);
  av[0].VStr:=planet.FGraphName;//from Main.dat Data.SE.Planet
end;

procedure SF_PlanetPopulation(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetPopulation');
  planet:=TPlanet(av[1].VDW);
  if(planet <> nil) then begin
    av[0].VInt:=planet.FPeopleCnt;
    if(High(av) > 1) then planet.FPeopleCnt:=av[2].VInt;
  end;
end;


procedure SF_PlanetOwner(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetOwner');
  planet:=TPlanet(av[1].VDW);
  if(planet <> nil) then begin
    av[0].VInt:=integer(planet.FOwner);
    if(High(av) > 1) then begin planet.FOwner:=TOwner(av[2].VInt); planet.CalcParam; end;
  end;
end;

procedure SF_PlanetRace(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetRace');
  planet:=TPlanet(av[1].VDW);
  if(planet <> nil) then begin
    av[0].VInt:=integer(planet.FRace);
    if(High(av) > 1) then planet.FRace:=tRace(av[2].VInt);
  end;
end;

procedure SF_PlanetGov(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetGov');
  planet:=TPlanet(av[1].VDW);
  if(planet <> nil) then begin
    av[0].VInt:=integer(planet.FGoverment);
    if(High(av) > 1) then planet.FGoverment:=TGoverment(av[2].VInt);
  end;
end;

procedure SF_PlanetEco(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetEco');
  planet:=TPlanet(av[1].VDW);
  if(planet <> nil) then begin
    av[0].VInt:=integer(planet.FEconomy);
    if(High(av) > 1) then planet.FEconomy:=TEconomy(av[2].VInt);
  end;
end;

procedure SF_PlanetTerrain(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  ttype:byte;
  val:integer;
  i:integer;
  gitem:PGoneItem;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script PlanetTerrain');
  planet:=TPlanet(av[1].VDW);
  ttype:=byte(av[2].VInt);
  case ttype of
    0: av[0].VInt:=planet.FWaterSpace;
    1: av[0].VInt:=planet.FLandSpace;
    2: av[0].VInt:=planet.FHillSpace;
    else raise Exception.Create('Error.Script PlanetTerrain ttype');
  end;
  if (High(av) > 2) then
  begin
    val:=av[3].VInt;
    case ttype of
      0: planet.FWaterSpace:=val;
      1: planet.FLandSpace:=val;
      2: planet.FHillSpace:=val;
    end;
    if planet.FGoneItems = nil then exit;
    for i:=0 to planet.FGoneItems.Count-1 do
    begin
      gitem:=planet.FGoneItems.Items[i];
      if gitem.FLandType <> ttype then continue;
      gitem.FRegion:=min(gitem.FRegion,val);
    end;
  end;
end;

procedure SF_PlanetTerrainExplored(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  ttype:byte;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script PlanetTerrainExplored');
  planet:=TPlanet(av[1].VDW);
  ttype:=byte(av[2].VInt);
  case ttype of
    0: av[0].VInt:=planet.FWaterComplate;
    1: av[0].VInt:=planet.FLandComplate;
    2: av[0].VInt:=planet.FHillComplate;
    else raise Exception.Create('Error.Script PlanetTerrainExplored ttype');
  end;
  if (High(av) > 2) then
  begin
    case ttype of
      0: planet.FWaterComplate:=av[3].VInt;
      1: planet.FLandComplate:=av[3].VInt;
      2: planet.FHillComplate:=av[3].VInt;
    end;
  end;
end;

procedure SF_PlanetOrbitRadius(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetOrbitRadius');
  planet:=TPlanet(av[1].VDW);
  av[0].VInt:=round(planet.FPolarPos.Radius);
  if(High(av) > 1) then planet.FPolarPos.Radius:=av[2].VInt;
end;

procedure SF_PlanetOrbitalVelocity(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetOrbitalVelocity');
  planet:=TPlanet(av[1].VDW);
  av[0].VInt:=round(10*planet.FAngle);//grads per 10 turns, setting 3600 means full circle in one turn
  if(High(av) > 1) then planet.FAngle:=0.1*av[2].VInt;
end;

procedure SF_PlanetSize(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetSize');
  planet:=TPlanet(av[1].VDW);
  av[0].VInt:=planet.FRadius;
  if(High(av) > 1) then
  begin
    planet.FRadius:=av[2].VInt;
    //pointless to change graph size
    //planet.FGraphRadius:=av[2].VInt;
  end;
end;

procedure SF_PlanetCurInvention(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetCurInvention');
  planet:=TPlanet(av[1].VDW);
  av[0].VInt:=ord(planet.FScn.CurrentInvention);
  if(High(av) > 1) then planet.FScn.CurrentInvention:=TInvention(av[2].VInt);
   {HullAlloy, FuelTanksType,
    EngineSpeed, RadarRadius,
    ScanerType, RepairRobotType,
    CargoHookType, TechLevel,
    Weapon1, Weapon2 ... Weapon12}
end;

procedure SF_PlanetCurInventionPoints(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetCurInventionPoints');
  planet:=TPlanet(av[1].VDW);
  av[0].VFloat:=planet.FScn.OpenPointsInvention;
  if(High(av) > 1) then planet.FScn.OpenPointsInvention:=av[2].VFloat;//0..100
end;

procedure SF_PlanetInventionLevel(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  inv:TInvention;
begin
  if High(av) < 2 then raise Exception.Create('Error.Script PlanetInventionLevel');
  planet:=TPlanet(av[1].VDW);
  inv:=TInvention(av[2].VInt);

  av[0].VInt:=planet.FScn.mOpenInvention[inv];

  if High(av) > 2 then planet.FScn.mOpenInvention[inv]:=av[3].VInt;//1..8
end;

procedure SF_PlanetBoostInventions(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  cnt,i:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetBoostInventions');
  planet:=TPlanet(av[1].VDW);
  if(High(av) > 1) then cnt:=av[2].VInt else cnt:=1;
  for i:=1 to cnt do planet.OpenInventions;
end;

procedure SF_PlanetWarriors(av:array of TVarEC; code:TCodeEC);
var
  planet: TPlanet;
  no:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetWarriors');
  planet:=TPlanet(av[1].VDW);
  if(High(av) = 1) then av[0].VInt:=planet.FWarriors.Count
  else begin
    no:=av[2].VInt;
    if(no >= 0) and (no < planet.FWarriors.Count) then av[0].VDW:=Cardinal(planet.FWarriors.Items[no]) else av[0].VDW:=0;
  end;

end;


procedure SF_GalaxySectors(av:array of TVarEC; code:TCodeEC);
var
  no: integer;
begin
  if(High(av) = 0) then begin
    av[0].VInt:=Galaxy.FConstellation.Count;
  end else begin
    no:=av[1].VInt;
    if(no >= 0) and (no < Galaxy.FConstellation.Count) then av[0].VDW:=Cardinal(Galaxy.FConstellation.Items[no]) else av[0].VDW:=0;
  end;
end;


procedure SF_GalaxyTechLevel(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=integer(Galaxy.FTechLevel);
end;

procedure SF_GalaxyDominatorResearchPercent(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then
  begin
    av[0].VInt:=Round((Galaxy.FScnBase[t_Blazer].Percent+
                       Galaxy.FScnBase[t_Keller].Percent+
                       Galaxy.FScnBase[t_Terron].Percent )/3);
  end else begin
    av[0].VInt:=Round(Galaxy.FScnBase[TDominatorSeries(av[1].VInt)].Percent);
    if(High(av) > 1) then Galaxy.FScnBase[TDominatorSeries(av[1].VInt)].Percent:=av[2].VInt;
  end;
end;

procedure SF_GalaxyDominatorResearchMaterial(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script GalaxyDominatorResearchMaterial');
  av[0].VInt:=Galaxy.FScnBase[TDominatorSeries(av[1].VInt)].Material;
  if(High(av) > 1) then Galaxy.FScnBase[TDominatorSeries(av[1].VInt)].Material:=av[2].VInt;
end;


procedure SF_GalaxyDiffLevels(av:array of TVarEC; code:TCodeEC);
var
  i, sum: integer;
begin
  if(High(av) > 0) then begin
    av[0].VInt:=50*(1+integer(Galaxy.FDifLevels[TDifLevelItems(av[1].VInt)]));
  end else begin
    sum:=0;
    for i:=0 to 7 do sum:=sum+50*(1+integer(Galaxy.FDifLevels[TDifLevelItems(i)]));
    av[0].VInt:=Round(sum*0.125);
  end;
end;




procedure SF_SectorVisible(av:array of TVarEC; code:TCodeEC);
var
  sector: TConstellation;
  i:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script SectorVisible');
  sector:=TConstellation(av[1].VDW);
  if(sector <> nil) then begin
    av[0].VInt:=integer(sector.FVisible);
    if(High(av) > 1) then sector.FVisible:=(av[2].VInt <> 0);
  end;

  if (High(av) > 1) and (av[2].VInt=1) and (Planet_PirateClan<>nil) and (sector=Planet_PirateClan.FStar.FConstellation) then
     for i:=0 to Galaxy.FConstellation.Count-1 do TConstellation(Galaxy.FConstellation.Items[i]).RestoreHiddenForm;
end;


procedure SF_HullHP(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  hull: THull;
  ship:TShip;
  val:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script HullHP');
  av[0].VInt:=0;
  obj:=TObject(av[1].VDW);
  if(obj is TShip) then hull:=TShip(obj).FHull
  else if(obj is THull) then hull:=THull(obj)
  else if (obj is TScriptItem) and ((obj as TScriptItem).FItem is THull) then hull:=(obj as TScriptItem).FItem as THull
  else exit;
  av[0].VInt:=hull.FHitPoints;
  if(High(av) > 1) then
  begin
    if av[2].VType = vtStr then
    begin
      val:=round(hull.FSize*(0.01*av[2].VInt));
      if Pos('UpTo',av[2].VStr)=1 then hull.FHitPoints:=max(hull.FHitPoints,val)
      else if Pos('DownTo',av[2].VStr)=1 then hull.FHitPoints:=min(hull.FHitPoints,val)
      else if Pos('To',av[2].VStr)=1 then hull.FHitPoints:=val
      else if Pos('Plus',av[2].VStr)=1 then hull.FHitPoints:=max(hull.FHitPoints,min(hull.FSize,hull.FHitPoints+val))
      else if Pos('Minus',av[2].VStr)=1 then hull.FHitPoints:=hull.FHitPoints-val
      else raise Exception.Create('Error.Script HullHP - unknown key '+av[2].VStr);

    end else begin
      hull.FHitPoints:=av[2].VInt;

    end;

    if obj is TShip then ship:=TShip(obj) else ship:=TShip(hull.FShip);
    if (ship<>nil) and ship.IsDestroyed and not ship.FShipDestroy then
    begin
      if (av[0].VInt>0) then ship.ScriptItemsAct(t_OnDeath);
      if (ship.FCurStar<>nil) and ship.FCurStar.FFilmBuild then ship.FCurStar.DelTargetShip(obj);
    end;
  end;
end;

procedure SF_HullDamageSuspectibility(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  hull: THull;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script HullDamageSuspectibility');
  av[0].VInt:=0;
  obj:=TObject(av[1].VDW);

  if(obj is TShip) then hull:=TShip(obj).FHull
  else if(obj is THull) then hull:=THull(obj)
  else if (obj is TScriptItem) and ((obj as TScriptItem).FItem is THull) then hull:=(obj as TScriptItem).FItem as THull
  else exit;

  av[0].VInt:=round(100*hull.Fragility([TDamageType(av[2].VDW)]));//0-en,1-sp,2-mi or just damage set
end;

procedure SF_HullType(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  hull: THull;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script HullType');
  av[0].VInt:=0;
  obj:=TObject(av[1].VDW);
  if(obj is TShip) then hull:=TShip(obj).FHull
  else if(obj is THull) then hull:=THull(obj)
  else if (obj is TScriptItem) and ((obj as TScriptItem).FItem is THull) then hull:=(obj as TScriptItem).FItem as THull
  else exit;
  av[0].VInt:=integer(hull.FShipType);
  if(High(av) > 1) then hull.FShipType:=TSShipType(av[2].VInt);
end;

procedure SF_HullSpecial(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  hull: THull;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script HullSpecial');
  av[0].VInt:=0;
  obj:=TObject(av[1].VDW);
  if(obj is TShip) then hull:=TShip(obj).FHull
  else if(obj is THull) then hull:=THull(obj)
  else if (obj is TScriptItem) and ((obj as TScriptItem).FItem is THull) then hull:=(obj as TScriptItem).FItem as THull
  else exit;
  av[0].VInt:=integer(hull.FSpecial-1);
  if(High(av) > 1) then hull.FSpecial:=av[2].VInt+1;
end;

procedure SF_HullSeries(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  hull: THull;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script HullSeries');
  av[0].VInt:=0;
  obj:=TObject(av[1].VDW);
  if(obj is TShip) then hull:=TShip(obj).FHull
  else if(obj is THull) then hull:=THull(obj)
  else if (obj is TScriptItem) and ((obj as TScriptItem).FItem is THull) then hull:=(obj as TScriptItem).FItem as THull
  else exit;
  av[0].VInt:=hull.FSeries; //now -1 is no series (was 255)
  if(High(av) > 1) then hull.FSeries:=av[2].VInt;
end;


procedure SF_GalaxyHoles(av:array of TVarEC; code:TCodeEC);
var
  no: integer;
begin
  if(High(av) = 0) then begin
    av[0].VInt:=Galaxy.FHoles.Count;
  end else begin
    no:=av[1].VInt;
    if(no >= 0) and (no < Galaxy.FHoles.Count) then av[0].VDW:=Cardinal(Galaxy.FHoles.Items[no]) else av[0].VDW:=0;
  end;
end;


procedure SF_HoleCreate2(av:array of TVarEC; code:TCodeEC);
var
  hole: THole;
  a,r: single;
  star1,star2: TStar;
  lFilmObj:TEFilmObj;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script HoleCreate2');
  star1:=TStar(av[1].VDW);
  star2:=TStar(av[2].VDW);

  hole:=THole.Create;
  hole.Init;
  hole.FGraphHole.State:=1;
  hole.FTurnCreate:=Galaxy.FTurn;
  hole.FType:=1;

  hole.FStar1:=star1;
  hole.FStar2:=star2;

  a:=Angle360ToRad(Rnd(0,359,Galaxy.FRndOut));
  r:=Rnd(1000,2000,Galaxy.FRndOut);

  hole.FPos1.x:=r*sin(a);
  hole.FPos1.y:=-r*cos(a);

  a:=Angle360ToRad(Rnd(0,359,Galaxy.FRndOut));
  r:=Rnd(1000,2000,Galaxy.FRndOut);

  hole.FPos2.x:=r*sin(a);
  hole.FPos2.y:=-r*cos(a);

  Galaxy.FHoles.Add(hole);
  av[0].VDW:=Cardinal(hole);

  if hole.FStar1.FFilmBuild or hole.FStar2.FFilmBuild then
  begin
		lFilmObj:=GFilm.ObjAdd(hole.FId,hole.FGraphHole,'','');
    GFilm.OrderMove(0,lFilmObj,hole.FPos1);
    GFilm.OrderHoleState(0,lFilmObj,1);
    GFilm.OrderGraphConnect(0,lFilmObj);
  end else if Player.InNormalSpace and ((Player.FCurStar=hole.FStar1) or (Player.FCurStar=hole.FStar2)) then GFormStarMap.FOpenHole := hole;
end;



procedure SF_HoleStar1(av:array of TVarEC; code:TCodeEC);
var
  hole: THole;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script HoleStar1');
  hole:=THole(av[1].VDW);
  if(hole <> nil) then begin
    av[0].VDW:=Cardinal(hole.FStar1);
    if(High(av) > 1) then hole.FStar1:=TStar(av[2].VDW);
  end;
end;

procedure SF_HoleStar2(av:array of TVarEC; code:TCodeEC);
var
  hole: THole;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script HoleStar2');
  hole:=THole(av[1].VDW);
  if(hole <> nil) then begin
    av[0].VDW:=Cardinal(hole.FStar2);
    if(High(av) > 1) then hole.FStar2:=TStar(av[2].VDW);
  end;
end;

procedure SF_HoleX1(av:array of TVarEC; code:TCodeEC);
var
  hole: THole;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script HoleX1');
  hole:=THole(av[1].VDW);
  if(hole <> nil) then begin
    av[0].VInt:=Round(hole.FPos1.X);
    if(High(av) > 1) then hole.FPos1.X:=av[2].VInt;
  end;
end;

procedure SF_HoleY1(av:array of TVarEC; code:TCodeEC);
var
  hole: THole;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script HoleY1');
  hole:=THole(av[1].VDW);
  if(hole <> nil) then begin
    av[0].VInt:=Round(hole.FPos1.Y);
    if(High(av) > 1) then hole.FPos1.Y:=av[2].VInt;
  end;
end;

procedure SF_HoleX2(av:array of TVarEC; code:TCodeEC);
var
  hole: THole;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script HoleX2');
  hole:=THole(av[1].VDW);
  if(hole <> nil) then begin
    av[0].VInt:=Round(hole.FPos2.X);
    if(High(av) > 1) then hole.FPos2.X:=av[2].VInt;
  end;
end;

procedure SF_HoleY2(av:array of TVarEC; code:TCodeEC);
var
  hole: THole;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script HoleY2');
  hole:=THole(av[1].VDW);
  if(hole <> nil) then begin
    av[0].VInt:=Round(hole.FPos2.Y);
    if(High(av) > 1) then hole.FPos2.Y:=av[2].VInt;
  end;
end;

procedure SF_HoleTurnCreate(av:array of TVarEC; code:TCodeEC);
var
  hole: THole;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script HoleTurnCreate');
  hole:=THole(av[1].VDW);
  av[0].VInt:=0;
  if(hole <> nil) then begin
    av[0].VInt:=hole.FTurnCreate;
    if(High(av) > 1) then hole.FTurnCreate:=av[2].VInt;
  end;
end;

procedure SF_HoleMap(av:array of TVarEC; code:TCodeEC);
var
  hole: THole;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script HoleMap');
  hole:=THole(av[1].VDW);
  if(hole <> nil) then begin
    av[0].VStr:=hole.FABMapName;
    if(High(av) > 1) then hole.FABMapName:=av[2].VStr;
  end else av[0].VStr:='';
  //special names - 'SkipAB','NoEntry'
end;

procedure SF_StarRuins(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  ship: TShip;
  i,counter:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script StarRuins');
  star:=TStar(av[1].VDW);
  if star = nil then exit;
  counter:=-1;

  if(High(av) = 1) then
  begin
    for i:=0 to star.FShips.Count-1 do
    begin
      ship:=star.FShips.Items[i];
      if ship is TRuins then counter:=counter + 1;
    end;
    av[0].VInt:=counter + 1;
    exit;
  end;

  if (av[2].VType=vtStr) then
  begin

    for i:=0 to star.FShips.Count-1 do
    begin
      ship:=star.FShips.Items[i];
      if ship is TRuins then
      begin
        if ((ship.FCustomTypeName<>'') and (ship.FCustomTypeName=av[2].VStr)) or
           ((ship.FCustomTypeName='')  and (mShipType[ship.FShipType].SysName=av[2].VStr)) then
        begin
          av[0].VDW:=Cardinal(ship);
          exit;
        end;
      end;
    end;

  end else begin

    for i:=0 to star.FShips.Count-1 do
    begin
      ship:=star.FShips.Items[i];
      if ship is TRuins then
      begin
        counter:=counter + 1;
        if counter = av[2].VInt then
        begin
          av[0].VDW:=Cardinal(ship);
          exit;
        end;
      end;
    end;
  end;
  av[0].VDW:=0;
end;


procedure SF_CreateQuestItem(av:array of TVarEC; code:TCodeEC);
var
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script CreateQuestItem');
  item:=TUselessItem.Create();
  (item as TUselessItem).Init(av[1].VStr,TDominatorSeries(0));
  if(High(av) > 1) then item.FOwner:=TOwner(av[2].VInt)
  else item.FOwner:=None;
  av[0].VDW:=Cardinal(item);
end;


procedure SF_ShipTurnBeforeEndOrder(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipTurnBeforeEndOrder');
  ship:=TShip(av[1].VDW);
  av[0].VInt:=ship.TurnBeforeEndOrder();
end;

procedure SF_ShipOrder(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipOrder');
  ship:=TShip(av[1].VDW);

  if (High(av)>1) and (av[2].VType=vtStr) then
  begin
    if av[2].VStr='X' then
    begin
      av[0].VFloat:=ship.FOrderDes.X;
      if High(av) > 2 then ship.FOrderDes.X:=av[3].VFloat;
    end else if av[2].VStr='Y' then
    begin
      av[0].VFloat:=ship.FOrderDes.Y;
      if High(av) > 2 then ship.FOrderDes.Y:=av[3].VFloat;
    end else raise Exception.Create('Error.Script ShipOrder - unknown key '+av[2].VStr);
    exit;
  end;

  if (ship=Player) and (AutoBattleShip<>nil) then av[0].VInt:=-1
  else av[0].VInt:=integer(ship.FOrder);
  if(High(av) > 1) then ship.FOrder:=TOrderType(av[2].VDW);
end;

procedure SF_ShipOrderData1(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
  dat1,dat2:word;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipOrderData1');
  ship:=TShip(av[1].VDW);
  dat2:=integer(ship.FOrderData) shr 16;
  dat1:=integer(ship.FOrderData) and $ffff;
  av[0].VInt:=dat1;
  if(High(av) > 1) then ship.FOrderData:=Cardinal((av[2].VInt and $ffff) + (dat2 shl 16));
end;


procedure SF_ShipOrderData2(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
  dat1,dat2:word;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipOrderData2');
  ship:=TShip(av[1].VDW);
  dat2:=integer(ship.FOrderData) shr 16;
  dat1:=integer(ship.FOrderData) and $ffff;
  av[0].VInt:=dat2;
  if(High(av) > 1) then ship.FOrderData:=Cardinal(dat1 + ((av[2].VInt and $ffff) shl 16));
end;


procedure SF_ShipOrderObj(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipOrderObj');
  ship:=TShip(av[1].VDW);
  if(ship <> nil) then
  begin
    if (ship=Player) and (AutoBattleShip<>nil) then av[0].VDW:=Cardinal(AutoBattleShip)
    else av[0].VDW:=Cardinal(ship.FOrderObj);
    if(High(av) > 1) then
    begin
      if (ship=Player) and (AutoBattleShip<>nil) then AutoBattleShip:=TShip(av[2].VDW)
      else ship.FOrderObj:=TObject(av[2].VDW);
    end;
  end;
end;

procedure SF_ShipDestination(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipDestination');
  ship:=TShip(av[1].VDW);
  if ship <> nil then
  begin
    if ship = Player then //used in jumps from dominion
    begin
      av[0].VDW:=Cardinal(Player.FFlyToStar);
      if High(av) > 1 then Player.FFlyToStar:=TStar(av[2].VDW);
    end
    else if ship is TRuins then //used by military bases and dominions
    begin
      av[0].VDW:=Cardinal(TRuins(ship).FFlyToStar);
      if High(av) > 1 then TRuins(ship).FFlyToStar:=TStar(av[2].VDW);
    end
    else
      av[0].VDW:=0;
  end;
end;

procedure SF_BuildRuins(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  ruins: TRuins;
  ruinstype: integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script BuildRuins');
  star:=TStar(av[1].VDW);
  if(star <> nil) then begin
    ruins:=nil;
    ruinstype:=av[2].VInt;
    if TShipType(ruinstype) in SetShipTypeRuinsAll then
    begin
      ruins:=TRuins.Create;
      ruins.Init(TShipType(ruinstype),star);
    end;
    av[0].VDW:=Cardinal(ruins);
  end;
end;

procedure SF_BuildCustomRuins(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
  ruins: TRuins;
begin
  if High(av) < 2 then raise Exception.Create('Error.Script BuildCustomRuins');
  star:=TStar(av[1].VDW);
  if(star <> nil) then
  begin
    ruins:=TRuins.Create;
    av[0].VDW:=Cardinal(ruins);
    ruins.Init(t_UB,star);//initialized as RC, so will have coalition owner and eq at creation
    ruins.FCustomTypeName:=av[2].VStr;
    if High(av) > 2 then ruins.FCurStanding:=TStanding(av[3].VInt)
    else ruins.FCurStanding:=tst_None;
  end;
  //standing defines relations, system captures, ships allowed to land
  //standing types:
  //0 - tst_Kling, counts as dominator, but unless is really TKling, does not have series, so will be enemy of other dominators too
  //1 - tst_None, no effect on system ownership at all (like Tranklucator without master)
  //2 - tst_CoalMilitary, same as Warriors, WB, RC
  //3 - tst_CoalActive, almost the same as Military, less pirate rank points, better relation with non-military type pirates (like SB, BK)
  //4 - tst_CoalPassive, tolerated by pirates (like transports that didn't kill pirate ships in current systems)
  //5 - tst_Neutral, no effect on coal-pirate war, but will defend against dominators (MC, reprogrammed Blazer, imprisoned ships)
  //6 - tst_PiratePassive, tolerated by coals (PB, normal pirates)
  //7 - tst_PirateActive, scavenger pirates that are attacking (so can capture system)
  //8 - tst_PirateMilitary, military pirates, CB, will not allow coalition-sided player to land
  //9 - tst_Custom, custom, hostile to everything except ships with same CustomFraction (and to completely everything if does not have faction)
  //note: adding ruin to custom faction will set standing as Custom and it will remain even if later faction gets cleared
end;


procedure SF_RuinsChangeType(av:array of TVarEC; code:TCodeEC);
var
  obj:TObject;
  ruin: TRuins;
  i,no,rtype:integer;
  ru:TShipType;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script RuinsChangeType');
  obj:=TObject(av[1].VDW);
  if not (obj is TRuins) then exit;
  ruin:=TRuins(obj);

  if (av[2].VType=vtStr) then
  begin
    for ru:=RuinFirstInList to RuinLastInListEx do
    begin
      if av[2].VStr=mShipType[ru].SysName then
      begin
        ruin.FShipType:=ru;
        exit;
      end;
    end;
  end;

  no:=av[2].VInt;
  ru:=TShipType(no);
  if not (ru in SetShipTypeRuinsAll) then exit;
  ruin.FShipType:=ru;
end;

procedure SF_ShipStanding(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
  ruins: TRuins;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script ShipStanding');
  ship:=TShip(av[1].VDW);
  if(ship <> nil) then
  begin
    av[0].VInt:=integer(ship.FCurStanding);
    if High(av) > 1 then ship.FCurStanding:=TStanding(av[2].VInt)
  end;

end;

procedure SF_ShipSlots(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ShipSlots');
  ship:=TShip(av[1].VDW);
  av[0].VInt:=0;
  if ship = nil then exit;

  case av[2].VInt of
    1: av[0].VInt := ship.SlotCount(st_Weapon);
    2: av[0].VInt := ship.SlotCount(st_Artefact);
    3: av[0].VInt := ship.SlotCount(st_Radar);
    4: av[0].VInt := ship.SlotCount(st_Scaner);
    5: av[0].VInt := ship.SlotCount(st_RepairRobot);
    6: av[0].VInt := ship.SlotCount(st_CargoHook);
    7: av[0].VInt := ship.SlotCount(st_DefGenerator);
    8: av[0].VInt := ship.SlotCount(st_Forsage);
  end;
end;

procedure SF_MissileStar(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script MissileStar');
  av[0].VDW := Cardinal(TMissile(av[1].VDW).FStar);
end;

procedure SF_MissileType(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script MissileType');
  av[0].VInt := integer(TMissile(av[1].VDW).FWeaponType);
end;

procedure SF_CustomMissileType(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script CustomMissileType');
  av[0].VStr := TMissile(av[1].VDW).WeaponInfo.SysName;
end;

procedure SF_MissileOwner(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script MissileOwner');
  av[0].VDW := Cardinal(TMissile(av[1].VDW).FFromShip);
  if High(av) > 1 then TMissile(av[1].VDW).FFromShip := TShip(av[2].VDW);
end;

procedure SF_MissileWeaponID(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script MissileWeaponID');
  av[0].VDW := TMissile(av[1].VDW).FWeaponID;
end;

procedure SF_MissileTarget(av:array of TVarEC; code:TCodeEC);
var
  mi:TMissile;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script MissileTarget');
  mi:=TMissile(av[1].VDW);
  if mi.FTarget<>nil then av[0].VDW := Cardinal(mi.FTarget)
  else av[0].VDW := Cardinal(mi.FTargetLost);
  if High(av) > 1 then TMissile(av[1].VDW).FTarget := TObject(av[2].VDW);
end;

procedure SF_MissileMaxDamage(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script MissileMaxDamage');
  av[0].VInt := TMissile(av[1].VDW).FMaxDamage;
  if High(av) > 1 then TMissile(av[1].VDW).FMaxDamage := av[2].VInt;
end;

procedure SF_MissileMinDamage(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script MissileMinDamage');
  av[0].VInt := TMissile(av[1].VDW).FMinDamage;
  if High(av) > 1 then TMissile(av[1].VDW).FMinDamage := av[2].VInt;
end;

procedure SF_MissileLive(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script MissileLive');
  av[0].VInt := TMissile(av[1].VDW).FLive;
  if High(av) > 1 then TMissile(av[1].VDW).FLive := av[2].VInt;
end;

procedure SF_MissileSpeed(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script MissileSpeed');

  av[0].VInt := round(TMissile(av[1].VDW).FSpeed);
  if High(av) > 1 then TMissile(av[1].VDW).FSpeed := av[2].VInt;
end;

procedure SF_MissileAngle(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script MissileAngle');
  av[0].VInt := round(TMissile(av[1].VDW).FAngle);//grad
  if High(av) > 1 then TMissile(av[1].VDW).FAngle := av[2].VInt;
end;


procedure SF_AsteroidMinerals(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script AsteroidMinerals');
  av[0].VInt := TAsteroid(av[1].VDW).FMinerals;
  if High(av) > 1 then TAsteroid(av[1].VDW).FMinerals := av[2].VInt;
end;

procedure SF_AsteroidGraph(av:array of TVarEC; code:TCodeEC);
var ast:TAsteroid;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script AsteroidGraph');
  ast:=TAsteroid(av[1].VDW);
  av[0].VStr := ast.FGraph.TypeO;
  if High(av) > 1 then
  begin
    DetachFromSE(TObjectSE(ast.FGraph));
    LinkToSE(TObjectSE(ast.FGraph),ObjCreateSE(GetStrParEC(av[2].VStr,0,'.'), av[2].VStr, Point(0,0)));
  end;
end;

procedure SF_AsteroidRespawn(av:array of TVarEC; code:TCodeEC);
var
  ast: TAsteroid;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script AsteroidRespawn');
  ast:=TAsteroid(av[1].VDW);
  if(ast <> nil) then ast.CalcNewRandomPar;
end;


// -----------------------------------------------------------------------------
// ---------------------------- ??????? ----------------------------------------
// -----------------------------------------------------------------------------
procedure SF_ArrayAdd(av:array of TVarEC; code:TCodeEC);
var
  el: TVarEC;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ArrayAdd');
  if(av[1].VType <> vtArray) then raise Exception.Create('Error.Script ArrayAdd - not array');
  el:=TVarEC.Create(av[2].VType);
  el.CopyFrom(av[2]);
  if High(av) > 2 then el.Name:=av[3].VStr;
  av[1].VArray.Add(el);

  av[0].VInt:=av[1].VArray.Count;
end;

procedure SF_ArrayDelete(av:array of TVarEC; code:TCodeEC);
var
  no: integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ArrayDelete');
  if(av[1].VType <> vtArray) then raise Exception.Create('Error.Script ArrayDelete - not array');
  no:=av[2].VInt;
  if (no >= 0) and (no < av[1].VArray.Count) then begin
    av[1].VArray.Del(no);
  end;
  av[0].VInt:=av[1].VArray.Count;
end;


procedure SF_ArrayClear(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ArrayClear');
  if(av[1].VType <> vtArray) then raise Exception.Create('Error.Script ArrayClear - not array');
  av[1].VArray.Clear();
  av[1].VArray.Add(TVarEC.Create(vtUnknown));
end;


procedure SF_ArrayDim(av:array of TVarEC; code:TCodeEC);
begin
  if High(av)<1 then raise Exception.Create('Error.Script ArrayDim');
  if(av[1].VType <> vtArray) then raise Exception.Create('Error.Script ArrayDim - not array');
  av[0].VInt:=av[1].VArray.Count;
end;


procedure SF_ArraySort(av:array of TVarEC; code:TCodeEC);
var
  arrnum,cnt,i,j,k:integer; //array1, array2, ...
  element:Cardinal;
begin
  arrnum:=High(av);
  if(arrnum < 1) then raise Exception.Create('Error.Script ArraySort');
  if(av[1].VType <> vtArray) then raise Exception.Create('Error.Script ArraySort - not array');

  cnt:=av[1].VArray.Count;
  if(cnt < 2) then exit;

  if(arrnum > 1) then begin
    for i:=2 to arrnum do begin
      if(av[i].VType <> vtArray) then raise Exception.Create('Error.Script ArraySort - type mismatch');
      if(av[i].VArray.Count <> cnt) then raise Exception.Create('Error.Script ArraySort - size mismatch');
    end;
  end;

  for i:=1 to cnt-1 do begin
    for j:=cnt-1 downto i do begin
      if(av[1].VArray.Items[j].VInt < av[1].VArray.Items[j-1].VInt) then begin
        for k:=1 to arrnum do begin
          element:=Cardinal(av[k].VArray.Items[j]);
          av[k].VArray.Items[j]:=av[k].VArray.Items[j-1];
          av[k].VArray.Items[j-1]:=TVarEC(element);
        end;
      end;
    end;
  end;
end;


procedure SF_ArraySortPartial(av:array of TVarEC; code:TCodeEC);
var
  arrnum,cnt,i,j,k,no:integer; //n, array1, array2, ...
  el: Cardinal;
begin
  arrnum:=High(av)-1;
  if(arrnum < 1) then raise Exception.Create('Error.Script ArraySortPartial');
  if(av[2].VType <> vtArray) then raise Exception.Create('Error.Script ArraySortPartial - not array');

  cnt:=av[2].VArray.Count;
  no:=av[1].VInt;
  if(cnt < 2) then exit;

  if(arrnum > 1) then begin
    for i:=2 to arrnum do begin
      if(av[i+1].VType <> vtArray) then raise Exception.Create('Error.Script ArraySortPartial - type mismatch');
      if(av[i+1].VArray.Count <> cnt) then raise Exception.Create('Error.Script ArraySortPartial - size mismatch');
    end;
  end;
  for j:=cnt-1 downto no do begin
    if(av[2].VArray.Items[j].VInt < av[2].VArray.Items[j-1].VInt) then begin
      for k:=1 to arrnum do begin
        el:=Cardinal(av[k+1].VArray.Items[j]);
        av[k+1].VArray.Items[j]:=av[k+1].VArray.Items[j-1];
        av[k+1].VArray.Items[j-1]:=TVarEC(el);
      end;
    end;
  end;
end;



procedure SF_ArrayRandomize(av:array of TVarEC; code:TCodeEC);
var
  arrmax,cnt,i,j1,j2,k,no:integer; //n, array1, array2, ...
  seed: Cardinal;
  el:pointer;
  useSeed:boolean;
begin
  arrmax:=High(av);
  if arrmax < 2 then raise Exception.Create('Error.Script ArrayRandomize');
  if av[2].VType <> vtArray then raise Exception.Create('Error.Script ArrayRandomize - not array');

  cnt:=av[2].VArray.Count;
  if cnt<2 then exit;

  no:=av[1].VInt;

  useSeed:=false;
  if av[arrmax].VType <> vtArray then
  begin
    seed:=av[arrmax].VDW;
    useSeed:=true;
    dec(arrmax);
  end;

  for i:=3 to arrmax do
   begin
   if av[i].VType <> vtArray then raise Exception.Create('Error.Script ArrayRandomize - type mismatch');
   if av[i].VArray.Count <> cnt then raise Exception.Create('Error.Script ArrayRandomize - size mismatch');
  end;

  for i:=1 to no do
  begin

    if useSeed then
    begin
      j1:=RndOut(0,cnt-1,seed);
      j2:=RndOut(0,cnt-1,seed);
    end else if Galaxy=nil then
    begin
      j1:=rnd(0,cnt-1);
      j2:=rnd(0,cnt-1);
    end else begin
      j1:=RndOut(0,cnt-1,Galaxy.FRndOut);
      j2:=RndOut(0,cnt-1,Galaxy.FRndOut);
    end;

    if j1<>j2 then
    begin
      for k:=2 to arrmax do
      begin
        el:=av[k].VArray.Items[j1];
        av[k].VArray.Items[j1]:=av[k].VArray.Items[j2];
        av[k].VArray.Items[j2]:=el;
      end;
    end;
  end;
end;



procedure SF_ArrayFind(av:array of TVarEC; code:TCodeEC);
var
  i:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ArrayFind');
  if(av[1].VType <> vtArray) then raise Exception.Create('Error.Script ArrayFind - not array');
  av[0].VInt:=-1;

  if av[2].VType = vtInt then
  begin
    for i:=0 to av[1].VArray.Count-1 do
      if av[1].VArray.Items[i].VInt = av[2].VInt then begin av[0].VInt:=i; exit; end;
  end
  else if av[2].VType = vtDW then
  begin
    for i:=0 to av[1].VArray.Count-1 do
      if av[1].VArray.Items[i].VDW = av[2].VDW then begin av[0].VInt:=i; exit; end;
  end
  else if av[2].VType = vtStr then
  begin
    for i:=0 to av[1].VArray.Count-1 do
      if av[1].VArray.Items[i].VStr = av[2].VStr then begin av[0].VInt:=i; exit; end;
  end
  else if av[2].VType = vtFloat then
  begin
    for i:=0 to av[1].VArray.Count-1 do
      if av[1].VArray.Items[i].VFloat = av[2].VFloat then begin av[0].VInt:=i; exit; end;
  end;
end;

procedure SF_ArrayFindInSorted(av:array of TVarEC; code:TCodeEC);
var
  cnt,value,vmax,vmin,imax,imin,vcur,icur,i,n,i_inc:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ArrayFindInSorted');
  if(av[1].VType <> vtArray) then raise Exception.Create('Error.Script ArrayFindInSorted - not array');
  icur:=0;
  vcur:=0;
  cnt:=av[1].VArray.Count;
  value:=av[2].VInt;
  imin:=0;vmin:=av[1].VArray.Items[0].VInt;
  imax:=cnt-1;vmax:=av[1].VArray.Items[cnt-1].VInt;
  n:=3;//n:=Round(0.5*ln(dim));

  if(value > vmax) or (value < vmin) then begin
    av[0].VInt:=-1;
    exit;
  end;

  if (value=vmax) then begin
    av[0].VInt:=imax;
    exit;
  end;
  if (value=vmin) then begin
    av[0].VInt:=imin;
    exit;
  end;
  if(vmax = vmin) then begin
    av[0].VInt:=-1;
    exit;
  end;


  for i:=1 to n do begin
    icur:=Round(imin+((value-vmin)*(imax-imin))/(vmax-vmin));
    vcur:=av[1].VArray.Items[icur].VInt;
    if(vcur > value) then begin
      imax:=icur;
      vmax:=vcur;
    end else begin
      imin:=icur;
      vmin:=vcur;
    end;
    if (value=vmax) then begin
      av[0].VInt:=imax;
      exit;
    end;
    if (value=vmin) then begin
      av[0].VInt:=imin;
      exit;
    end;
    if(vmax = vmin) then begin
      av[0].VInt:=-1;
      exit;
    end;
  end;


  if(icur = imax) then i_inc:=-1
  else i_inc:=1;

  icur:=icur+i_inc;
  vcur:=av[1].VArray.Items[icur].VInt;

  while((vcur <> value) and (icur < imax) and (icur > imin) and (i_inc * (value - vcur) > 0)) do begin
    icur:=icur+i_inc;
    vcur:=av[1].VArray.Items[icur].VInt;
  end;

  if vcur=value then av[0].VInt:=icur
  else av[0].VInt:=-1;
end;




procedure SF_DistToNearestEnemySystem(av:array of TVarEC; code:TCodeEC);
var
  i, dist: integer;
  star,star2: TStar;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script DistToNearestEnemySystem');
  star:=TStar(av[1].VDW);
  i:=0;
  dist:=0;
  while i < Galaxy.FStars.Count do
  begin
    star2:=star.FStarDist[i].FStar as TStar;
    if star2.FStatus.Owners = Klings then break;
    if star2.FStatus.CustomFaction <> '' then break;
    i:=i+1;
  end;
  if i = Galaxy.FStars.Count then av[0].VInt:=-1
  else av[0].VInt:=star.FStarDist[i].FDist;
end;





procedure SF_StarEnemyThreatLevel(av:array of TVarEC; code:TCodeEC);
var
  star,star2: TStar;
  ship:TShip;
  i,j:integer;
  st:TSetOfStanding;
  countPirates:boolean;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script StarEnemyThreatLeve');
  star:=TStar(av[1].VDW);

  countPirates:=(High(av)>1) and (av[2].VInt=1);

  if(star = nil) then raise Exception.Create('Error.Script StarEnemyThreatLevel');

  if(star.FStatus.Owners = Klings) or (star.FStatus.CustomFaction <> '') or (countPirates and (star.FStatus.Owners = Pirates)) then
  begin
    av[0].VInt:=3;
    exit;
  end;

  if star.FStatus.Battle then
  begin
    av[0].VInt:=2;
    exit;
  end;

  if Galaxy.FKellerAttackStar=star then
  begin
    av[0].VInt:=1;
    exit;
  end;

  st:=[tst_Kling,tst_Custom];
  if countPirates then st:=st+[tst_PirateMilitary,tst_PirateActive];

  for j:=0 to star.FShips.Count-1 do
  begin
    ship:=star.FShips.Items[j];
    if (ship.FCurPlanet<>nil) and (TPlanet(ship.FCurPlanet).FOwner=None) then continue;
    if ship.FCurStanding in st then
    begin
      av[0].VInt:=1;
      exit;
    end;
  end;

  for i:=1 to Galaxy.FStars.Count-1 do
  begin
    star2:=TStar(star.FStarDist[i].FStar);
    if(star2.FStatus.Owners = Klings) or (star.FStatus.CustomFaction <> '') or (countPirates and (star.FStatus.Owners = Pirates)) then
    begin
      for j:=0 to star2.FShips.Count-1 do
      begin
        ship:=star2.FShips.Items[j];
        if (ship.FOrderObj = star) and (ship.FCurStanding in st) then
        begin
          av[0].VInt:=1;
          exit;
        end;
        if (ship is TRuins) and (TRuins(ship).FFlyToStar=star) and (ship.FCurStanding in st) then
        begin
          av[0].VInt:=1;
          exit;
        end;
      end;
    end;
  end;

  av[0].VInt:=0;
end;



procedure SF_BuildListOfQuestPossibleLocations(av:array of TVarEC; code:TCodeEC);
var
  i,j,k,mindist,maxdist,cnt:integer;
  star,star2:TStar;
  flag:boolean;
  tempvar:TVarEC;
begin
  if(High(av) < 4) then raise Exception.Create('Error.Script BuildListOfQuestPossibleLocations');
  if(av[1].VType <> vtArray) then raise Exception.Create('Error.Script BuildListOfQuestPossibleLocations - not array');
  star:=TStar(av[2].VDW);
  mindist:=av[3].VInt;
  maxdist:=av[4].VInt;

  av[1].VArray.Clear();

  i:=1;
  while(i < Galaxy.FStars.Count) and (star.FStarDist[i].FDist <= maxdist) do begin
    star2:=TStar(star.FStarDist[i].FStar);
    if(star.FStarDist[i].FDist >= mindist) and (star2.FStatus.Owners = Normals) and (star2.FStatus.CustomFaction='')
      and (not star2.FStatus.Battle) and (star2 <> Galaxy.FKellerAttackStar)
      and (star2.Visible) then
    begin
      flag:=true;
      if(High(av) > 4) then
        for j:=5 to High(av) do
          if Cardinal(star2)=av[j].VDW then flag:=false;
      if flag then begin
        tempvar:=TVarEC.Create(vtDW);
        tempvar.VDW:=Cardinal(star2);
        av[1].VArray.Add(tempvar);
      end;
    end;
    i:=i+1;
  end;

  cnt:=av[1].VArray.Count;
  for i:=cnt-1 downto 0 do begin
    star:=TStar(av[1].VArray.Items[i].VDW);
    j:=0;
    flag:=true;
    while(flag and (j < star.FShips.Count)) do begin
      if(TShip(star.FShips.Items[j]).FShipType = t_Kling) then begin
        flag:=false;
        av[1].VArray.Del(i);
      end else j:=j+1;
    end;
  end;

  cnt:=av[1].VArray.Count;
  i:=0;
  while((i < Galaxy.FStars.Count) and (cnt > 0)) do begin
    star:=Galaxy.FStars.Items[i];
    if(star.FStatus.Owners = Klings) then begin
      for j:=0 to star.FShips.Count-1 do begin
        if(TShip(star.FShips.Items[j]).FShipType=t_Kling)
          and (TShip(star.FShips.Items[j]).FOrderObj is TStar) then begin

          star2:=TShip(star.FShips.Items[j]).FOrderObj as TStar;
          for k:=av[1].VArray.Count-1 downto 0 do begin
            if(av[1].VArray.Items[k].VDW = Cardinal(star2)) then begin
              av[1].VArray.Del(k);
              cnt:=av[1].VArray.Count;
            end;
          end;
        end;
      end;
    end;
    i:=i+1;
  end;

  cnt:=av[1].VArray.Count;
  av[0].VInt:=cnt;
  if(cnt = 0) then av[1].VArray.Add(TVarEC.Create(vtUnknown));
end;





procedure SF_FindItemInShip(av:array of TVarEC; code:TCodeEC);
var
  ship :TShip;
  item: TItem;
  obj: TObject;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script FindItemInShip');
  ship:=TShip(av[1].VDW);
  obj:=TObject(av[2].VDW);
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  av[0].VInt:=-1;
  if(item <> nil) then begin
    av[0].VInt:=ship.FEquipments.IndexOf(item);
    if(av[0].VInt < 0) then av[0].VInt:=ship.FArtefacts.IndexOf(item);
  end;
end;


procedure SF_GalaxyRangers(av:array of TVarEC; code:TCodeEC);
var
  no: integer;
begin
  if(High(av) = 0) then begin
    av[0].VInt:=Galaxy.FRangers.Count;
  end else begin
    no:=av[1].VInt;
    if(no >= 0) and (no < Galaxy.FRangers.Count) then av[0].VDW:=Cardinal(Galaxy.FRangers.Items[no]) else av[0].VDW:=0;
  end;
end;


procedure SF_MakeShipEnterStar(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
  starto,starfrom: TStar;
  delay: WORD;
  pos: TPos;
  no: integer;
  scriptorder: byte;
begin
  if(High(av) < 4) then raise Exception.Create('Error.Script MakeShipEnterStar');
  ship:=TShip(av[1].VDW);
  starto:=TStar(av[2].VDW);
  starfrom:=TStar(av[3].VDW);
  delay:=WORD(av[4].VDW);

  if (ship = Player) and Player.InPlanetOrShip then
  begin
    ShopListToEquipmentShop;
    ShopListDestroy;
  end;

  no:=ship.FCurStar.FShips.IndexOf(ship);
  if(no >= 0) then ship.FCurStar.FShips.Delete(no);

  ship.FCurStar:=starfrom;
  scriptorder:=ship.FScriptOrderAbsolute;
  ship.FScriptOrderAbsolute:=0;
  ship.OrderJump(starto, true);
  ship.FScriptOrderAbsolute:=scriptorder;

  starto.FShips.Add(ship);
  ship.FCurStar:=starto;
  ship.FOrderData:=delay;
  ship.FInHiperSpace:=true;
  ship.FPrevStar:=starfrom;

  ship.FAngle:=AngleCalc(starfrom.FPos,starto.FPos);

  if ship is TNormalShip then
    if (ship as TNormalShip).FLastPlanet=nil then
      (ship as TNormalShip).FLastPlanet:=(ship as TNormalShip).FHomePlanet;

  ship.FCurPlanet:=nil;
  ship.FCurShip:=nil;
end;



procedure SF_ShipGetBad(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipGetBad');
  if(av[1].VDW = 0) then Exit;
  av[0].VDW:=Cardinal(TShip(av[1].VDW).FShipBad);
end;


procedure SF_ShipAddDropItem(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
  item: TItem;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ShipAddDropItem');
  ship:=TShip(av[1].VDW);
  item:=TItem(av[2].VDW);

  if(ship <> nil) and (item <> nil) then begin
    av[0].VInt:=ship.FDropEq.Add(item);
  end;
end;


procedure SF_BonusCount(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=GCntMicroModuls;
end;

procedure SF_SeriesCount(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=GCntHullType;
end;

procedure SF_BonusPriority(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script BonusPriority');
  if(av[1].VInt < 0) or (av[1].VInt >= GCntMicroModuls) then raise Exception.Create('Error.Script BonusPriority - number out of range');
  av[0].VInt:=integer(mMicroModuls[av[1].VInt].Priority);
end;

procedure SF_BonusIsSpecial(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script BonusIsSpecial');
  if(av[1].VInt < 0) or (av[1].VInt >= GCntMicroModuls) then raise Exception.Create('Error.Script BonusIsSpecial - number out of range');
  av[0].VInt:=ord(mMicroModuls[av[1].VInt].Special);
end;


procedure SF_BonusName(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script BonusName');
  if(av[1].VInt < 0) or (av[1].VInt >= GCntMicroModuls) then raise Exception.Create('Error.Script BonusName - number out of range');
  av[0].VStr:=mMicroModuls[av[1].VInt].Name;
end;

procedure SF_BonusNumInCfg(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script BonusNumInCfg');
  if av[1].VInt = -1 then begin av[0].VStr:=''; exit; end;
  if(av[1].VInt < 0) or (av[1].VInt >= GCntMicroModuls) then raise Exception.Create('Error.Script BonusNumInCfg - number out of range');
  av[0].VStr{VInt}:=mMicroModuls[av[1].VInt].BlockNameInCfg;//NumInCfg;
end;

procedure SF_SeriesNumInCfg(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script SeriesNumInCfg');
  if av[1].VInt = -1 then begin av[0].VStr:=''; exit; end;
  if(av[1].VInt < 0) or (av[1].VInt >= GCntHullType) then raise Exception.Create('Error.Script SeriesNumInCfg - number out of range');
  av[0].VStr{VInt}:=mHullType[av[1].VInt].BlockNameInCfg;//NumInCfg;
end;

procedure SF_BonusValue(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script BonusValue');
  if(av[1].VInt < 0) or (av[1].VInt >= GCntMicroModuls) then raise Exception.Create('Error.Script BonusValue - number out of range');
  av[0].VInt:=mMicroModuls[av[1].VInt].mBonus[TBonusItem(av[2].VInt)];
end;

procedure SF_FindBonusByName(av:array of TVarEC; code:TCodeEC);
var
  i: integer;
begin
  if High(av)<1 then raise Exception.Create('Error.Script FindBonusByName');
  av[0].VInt:=-1;
  for i:=0 to High(mMicroModuls) do
    if mMicroModuls[i].Name=av[1].VStr then begin av[0].VInt:=i; exit; end;
end;

procedure SF_FindSeriesByName(av:array of TVarEC; code:TCodeEC);
var
  i: integer;
begin
  if High(av)<1 then raise Exception.Create('Error.Script FindSeriesByName');
  av[0].VInt:=-1;
  for i:=0 to High(mHullType) do
    if mHullType[i].Name=av[1].VStr then begin av[0].VInt:=i; exit; end;
end;


procedure SF_FindBonusByCustomTag(av:array of TVarEC; code:TCodeEC);
var
  i,j: integer;
begin
  if High(av)<1 then raise Exception.Create('Error.Script FindBonusByCustomTag');
  av[0].VInt:=-1;
  j:=0;

  if High(av)>1 then j:=av[2].VInt;
  for i:=0 to GCntMicroModuls-1 do
  begin
    if mMicroModuls[i].CustomTag<>av[1].VStr then Continue;
    if j=0 then begin av[0].VInt:=i; exit; end;
    Dec(j);
  end;

end;

procedure SF_FindBonusByNameInCfg(av:array of TVarEC; code:TCodeEC);
var
  i: integer;
begin
  if High(av)<1 then raise Exception.Create('Error.Script FindBonusByNameInCfg');
  av[0].VInt:=-1;

  for i:=0 to High(mMicroModuls) do
    if mMicroModuls[i].BlockNameInCfg=av[1].VStr then begin av[0].VInt:=i; exit; end;

end;

procedure SF_BonusCustomTag(av:array of TVarEC; code:TCodeEC);
var bp:TBlockParEC;
begin
  if High(av)<1 then raise Exception.Create('Error.Script BonusCustomTag');
  bp:=GR_BPLang.BlockPath['MicroModuls.' + mMicroModuls[av[1].VInt].BlockNameInCfg];
  if bp.Par_Count('CustomTag')<=0 then av[0].VStr:=''
  else av[0].VStr:=bp.ParPath_Get('CustomTag');
end;

procedure SF_CreateEquipmentWithSpecial(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
  itemtype:TItemType;
  setEq:TSetItemType;
  size,level:integer;
  owner:TOwner;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script CreateEquipmentWithSpecial');

  if not mMicromoduls[av[1].VInt].Special then raise Exception.Create('Error.Script CreateEquipmentWithSpecial - not special');
  setEq:=mMicromoduls[av[1].VInt].ItemType;

  itemtype:=RandomItemTypeFromSet(setEq,Galaxy.FRndOut);

  //size, level, owner
  if(High(av) > 3) then item:=CreateEq(itemtype,av[2].VInt,av[3].VInt,TOwner(av[4].VInt))
  else item:=CreateSimpleItemByType(itemtype);

  SpecialToEquipment(av[1].VInt, TEquipment(item));
  av[0].VDW:=Cardinal(item);
end;

procedure SF_SpecialToEquipment(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SpecialToEquipment');
  obj:=TObject(av[2].VDW);
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if av[1].VInt>=0 then
  begin
    TEquipment(item).FSpecial:=0;
    {if ((item is THull) and not BonusCompatibleWithHull(av[1].VInt,THull(item))) or
       ((item is TWeapon) and not BonusCompatibleWithWeapon(av[1].VInt,TWeapon(item))) or
       (not BonusCompatibleWithEq(av[1].VInt,TEquipment(item))) then
    begin
      SFT(CurCodeOwner+' adds '+ mMicromoduls[av[1].VInt].Name +' on '+ item.Name);
    end;}
    SpecialToEquipment(av[1].VInt, TEquipment(item));
  end else RemoveSpecialFromEquipment(TEquipment(item));
end;

procedure SF_ModuleToEquipment(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SpecialToEquipment');
  obj:=TObject(av[2].VDW);
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if av[1].VInt>=0 then
  begin
    TEquipment(item).FBonus:=0;
    MicroModuleToEquipment(av[1].VInt, TEquipment(item));
  end else RemoveMicroModuleFromEquipment(TEquipment(item));
end;

procedure SF_EqSpecial(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  eq: TEquipment;
  mi:TMissile;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script EqSpecial');
  av[0].VInt:=0;
  obj:=TObject(av[1].VDW);
  if obj is TMissile then
  begin
    mi:=TMissile(obj);
    av[0].VInt:=integer(mi.FSpecial-1);
    if(High(av) > 1) then mi.FSpecial:=av[2].VInt+1;
  end;

  if (obj is TEquipment) then eq:=TEquipment(obj)
  else if (obj is TScriptItem) and ((obj as TScriptItem).FItem is TEquipment) then eq:=(obj as TScriptItem).FItem as TEquipment
  else exit;
  av[0].VInt:=eq.FSpecial-1;
  if(High(av) > 1) then eq.FSpecial:=av[2].VInt+1;
end;

procedure SF_EqModule(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  eq: TEquipment;
  mi:TMissile;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script EqModule');
  av[0].VInt:=0;
  obj:=TObject(av[1].VDW);
  if obj is TMissile then
  begin
    mi:=TMissile(obj);
    av[0].VInt:=integer(mi.FBonus-1);
    if(High(av) > 1) then mi.FBonus:=av[2].VInt+1;
  end;

  if (obj is TEquipment) then eq:=TEquipment(obj)
  else if (obj is TScriptItem) and ((obj as TScriptItem).FItem is TEquipment) then eq:=(obj as TScriptItem).FItem as TEquipment
  else exit;
  av[0].VInt:=integer(eq.FBonus-1);
  if(High(av) > 1) then eq.FBonus:=av[2].VInt+1;
end;

procedure SF_MayAddBonusToEq(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  eq: TEquipment;
  no:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script MayAddModuleToEq');
  av[0].VInt:=0;

  no:=av[1].VInt;

  obj:=TObject(av[2].VDW);
  if (obj is TEquipment) then eq:=TEquipment(obj)
  else if (obj is TScriptItem) and ((obj as TScriptItem).FItem is TEquipment) then eq:=(obj as TScriptItem).FItem as TEquipment
  else exit;

  if (eq.FSpecial<>0) and mMicroModuls[eq.FSpecial-1].BlockMM then exit;

  if eq is TWeapon then av[0].VInt:=ord(BonusCompatibleWithWeapon(av[1].VInt,TWeapon(eq)))
  else if eq is THull then av[0].VInt:=ord(BonusCompatibleWithHull(av[1].VInt,THull(eq)))
  else av[0].VInt:=ord(BonusCompatibleWithEq(av[1].VInt,eq));
end;


procedure SF_BuildListOfMMByPriority(av:array of TVarEC; code:TCodeEC);
var
  i,minpr,maxpr,cnt:integer;
  tempvar:TVarEC;
  restrict:boolean;
begin
  if(High(av) < 3) then raise Exception.Create('Error.Script BuildListOfMMByPriority');
  if(av[1].VType <> vtArray) then raise Exception.Create('Error.Script BuildListOfMMByPriority - not array');

  if High(av)>3 then restrict:=(av[4].VInt<>0) else restrict:=true;

  if(av[2].VInt < av[3].VInt) then begin
    maxpr:=av[3].VInt;
    minpr:=av[2].VInt;
  end else begin
    maxpr:=av[2].VInt;
    minpr:=av[3].VInt;
  end;

  av[1].VArray.Clear();

  for i:=0 to GCntMicroModuls-1 do
  begin
    if mMicroModuls[i].Special then continue;

    if (integer(mMicroModuls[i].Priority) > maxpr) or
       (integer(mMicroModuls[i].Priority) < minpr) then continue;

    if mMicroModuls[i].RacialRestriction and restrict then continue;

    tempvar:=TVarEC.Create(vtInt);
    tempvar.VInt:=i;
    av[1].VArray.Add(tempvar);
  end;

  cnt:=av[1].VArray.Count;
  av[0].VInt:=cnt;
  if(cnt = 0) then av[1].VArray.Add(TVarEC.Create(vtUnknown));
end;

procedure SF_BuildListOfNewShips(av:array of TVarEC; code:TCodeEC);
var
  i,j,k,n,cnt:integer;
  startId,zn:Cardinal;
  star: TStar;
  planet: TPlanet;
  ship: TShip;
  sst:TSetShipType;
  so:TSetOwner;
  tempvar:TVarEC;
  addScriptShips:boolean;
  factionsList: array of WideString;
  cntFactions:integer;
  typesList: array of WideString;
  cntTypes:integer;
  tstr:WideString;

  procedure CheckShip(ship:TShip);
  var found:boolean;
      i:integer;
  begin
    if ship.FId < startId then exit;
    if not (ship.FShipType in sst) then exit;
    if ((ship.FScriptShip <> nil) or (ship.FScriptOrderAbsolute<>0)) and not addScriptShips then exit;
    if cntFactions>=0 then
    begin
      if ship.FScriptShip <> nil then tstr:=TScriptShip(ship.FScriptShip).FCustomFaction else tstr:='';
      if (cntFactions=0) and (tstr<>'') then exit;
      found:=(cntFactions=0);
      for i:=0 to cntFactions-1 do
        if tstr=factionsList[i] then begin found:=true; break; end;
      if not found then exit;

      if cntTypes>=0 then
      begin
        tstr:=ship.FCustomTypeName;
        if (cntTypes=0) and (tstr<>'') then exit;

        found:=(cntTypes=0);
        for i:=0 to cntTypes-1 do
          if tstr=typesList[i] then begin found:=true; break; end;
        if not found then exit;
      end;
    end;
    tempvar:=TVarEC.Create(vtInt);
    tempvar.VDW:=Cardinal(ship);
    av[1].VArray.Add(tempvar);
  end;

  procedure CheckItem(item:TItem);
  begin
    if (item=nil) or not (item is TArtefactTranclucator) then exit;
    CheckShip(TArtefactTranclucator(item).FShip as TShip);
  end;

begin
  if(High(av) < 2) then raise Exception.Create('Error.Script BuildListOfNewShips');
  if(av[1].VType <> vtArray) then raise Exception.Create('Error.Script BuildListOfNewShips - not array');
  av[1].VArray.Clear();

  startId:=av[2].VDW;

  if (High(av)>2) and (av[3].VDW<>0) then sst:=TSetShipType(Word(av[3].VDW))
  else sst:=SetShipTypeAll - [t_Tranclucator];

  if (High(av)>3) and (av[4].VDW<>0) then so:=TSetOwner(Byte(av[4].VDW))
  else so:=SetOwnerAll;

  addScriptShips:=false;
  if (High(av)>4) and (av[5].VInt<>0) then addScriptShips:=true;

  if High(av)>5 then
  begin
    tstr:=av[6].VStr;
    if tstr='' then
    begin
      cntFactions:=0;
      factionsList:=nil;
    end else begin
      cntFactions:=GetCountParEC(tstr,',');
      SetLength(factionsList,cntFactions);
      for i:=0 to cntFactions-1 do factionsList[i]:=GetStrParEC(tstr,i,',');
    end;

    if High(av)>6 then
    begin
      tstr:=av[7].VStr;
      if tstr='' then
      begin
        cntTypes:=0;
        typesList:=nil;
      end else begin
        cntTypes:=GetCountParEC(tstr,',');
        SetLength(typesList,cntTypes);
        for i:=0 to cntTypes-1 do typesList[i]:=GetStrParEC(tstr,i,',');
      end;
    end else begin
      typesList:=nil;
      cntTypes:=-1;
    end;

  end else begin
    factionsList:=nil;
    cntFactions:=-1;
    typesList:=nil;
    cntTypes:=-1;
  end;




  for i:=0 to Galaxy.FStars.Count-1 do
  begin
    star:=Galaxy.FStars[i];
    for j:=0 to star.FShips.Count-1 do
    begin
      ship:=star.FShips[j];
      if ship.FShipType = t_Warrior then continue;
      CheckShip(ship);
    end;

    if t_Warrior in sst then for j:=0 to star.FPlanets.Count-1 do
    begin
      planet:=star.FPlanets[j];
      for k:=0 to planet.FWarriors.Count-1 do
      begin
        ship:=planet.FWarriors[k];
        CheckShip(ship);
      end;
    end;
  end;


  if t_Tranclucator in sst then
  begin
    for i:=0 to Galaxy.FStars.Count-1 do
    begin
      star:=Galaxy.FStars[i];
      for j:=0 to star.FShips.Count-1 do
      begin
        ship:=star.FShips[j];
        if ship.FShipType = t_Warrior then continue;
        for k:=0 to ship.FArtefacts.Count-1 do CheckItem(ship.FArtefacts[k]);
      end;

      for j:=0 to star.FPlanets.Count-1 do
      begin
        planet:=star.FPlanets[j];
        for k:=0 to planet.FWarriors.Count-1 do
        begin
          ship:=planet.FWarriors[k];
          for n:=0 to ship.FArtefacts.Count-1 do CheckItem(ship.FArtefacts[n]);
        end;
      end;

      for j:=0 to star.FItems.Count-1 do CheckItem(star.FItems[j]);
      for j:=0 to star.FItemsDrop.Count-1 do CheckItem(PDropItem(star.FItemsDrop[j]).FItem as TItem);
    end;

    for i := 0 to Player.FStorage.Count - 1 do CheckItem(PStorageUnit(Player.FStorage.Items[i]).FItem);
  end;

  cnt:=av[1].VArray.Count;
  av[0].VInt:=cnt;
  if cnt = 0 then av[1].VArray.Add(TVarEC.Create(vtUnknown));
end;


procedure SF_PlanetToStar(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetToStar');
  av[0].VDW:=Cardinal(TPlanet(av[1].VDW).FStar);
end;


procedure SF_Chameleon(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script Chameleon');

  ship:=TShip(av[1].VDW);
  if(ship = nil) then ship:=Player;

  if(High(av) > 1) and (av[2].VStr <> '') then
  begin
    if av[2].VStr = 'GraphName' then
    begin
      av[0].VStr:=ship.FGraphShip.TypeO;
      exit;
    end;

    DetachFromSE(ship.FGraphShip);
    LinkToSE(ship.FGraphShip,ObjCreateSE(GetStrParEC(av[2].VStr,0,'.'), av[2].VStr, Point(0,0)));
    ship.FGraphName:=ship.FGraphShip.TypeO;
    ship.FGraphShip.Pos:=ship.FPos;
    ship.FGraphShip.Angle:=AngleGraTo256(ship.FAngle);
    ship.FGraphShip.Trans:=0;
    ship.FScriptChameleon:=true;
    ship.FChameleon:=false;
    ship.CalcParam();
    ship.CalcParamGraphSize();

  end else begin // ?????? ???????? ?? ??????, ????????? ???????? ???????
    ship.FScriptChameleon:=false;
    DetachFromSE(ship.FGraphShip);
    ship.GraphShipUpdate;
  end;

  // ???? ???? ?????? ???????? ? ?? ?? ????, ? ??????? ???? - ??????, ?? ????????????? ???? ???????, ????? ???????? ???? ???????
  if(High(av) > 2) and (av[3].VInt <> 0) and (GFormCur = mlf_StarMap) then begin
    GFormNext:=mlf_StarMap;
    TMessageLoopGI(GForm[GFormCur]).ExitLoop();
  end;
end;

procedure SF_IsChameleon(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script IsChameleon');

  ship:=TShip(av[1].VDW);
  if(ship = nil) then ship:=Player;

  if ship.FScriptChameleon then av[0].VInt:=1 else av[0].VInt:=0;
end;

procedure SF_PlayerChameleonCharges(av:array of TVarEC; code:TCodeEC);
var
  ser: TDominatorSeries;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script PlayerChameleonCharges');
  ser:=TDominatorSeries(av[1].VInt);
  av[0].VInt:=Player.FChameleonCharge[ser];
  if High(av) > 1 then Player.FChameleonCharge[ser]:=av[2].VInt;
end;

procedure SF_PlayerChameleonCurType(av:array of TVarEC; code:TCodeEC);
var
  ser: TDominatorSeries;
begin
  if not Player.FChameleon then av[0].VInt:=-1
  else av[0].VInt:=integer(Player.FChameleonSeries);

  if High(av) > 0 then
  begin
    if av[1].VInt<0 then Player.FChameleon:=false
    else begin
      Player.FChameleon:=true;
      Player.FChameleonSeries:=TDominatorSeries(av[1].VInt);
    end;
  end;
end;

procedure SF_PlayerChameleonDetected(av:array of TVarEC; code:TCodeEC);
var
  ser: TDominatorSeries;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script PlayerChameleonDetected');
  ser:=TDominatorSeries(av[1].VInt);
  av[0].VInt:=ord(Player.FChameleonDetect[ser]);
  if High(av) > 1 then Player.FChameleonDetect[ser]:=(av[2].VInt<>0);
end;


procedure SF_PlayerLogicChameleon(av:array of TVarEC; code:TCodeEC);
var
  ser: TDominatorSeries;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script PlayerLogicChameleon');
  ser:=TDominatorSeries(av[1].VInt);
  av[0].VInt:=Player.FChameleonLogic[ser];
  if High(av) > 1 then Player.FChameleonLogic[ser]:=av[2].VInt;
  //0 - normal logic
  //1 - dominators don't attack except when PlayerChameleonDetected
  //2 - dominators don't attack, Player can't attack first (but can defend when attacked somehow)
  //this function does not clear current ShipBad and PlayerChameleonDetected
  //dialogs are not affected by this (except overriding PlayerChameleonDetected in state 2)
end;


procedure SF_SwitchToMirrorImage(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
  hull: THull;
  tmpImage:TShip2SE;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SwitchToMirrorImage');

  ship:=TShip(av[1].VDW);
  if(ship = nil) then ship:=Player;
  hull:=ship.FHull;
  if hull.FShipType<>ts_AST then raise Exception.Create('Error.Script SwitchToMirrorImage: Not a special hull');
  hull.FSpecial:=av[2].VInt+1;

  if ship.FScriptChameleon or ship.FChameleon or ship.FGraphDominator then Exit;
  tmpImage:=ObjCreateSE('Ship2','Ship.Akrin.'+hull.GraphShipTypeAdon,Point(0,0)) as TShip2SE;
  tmpImage.CopyDataFromMirrorImage(ship.FGraphShip);
  tmpImage.Free;
  tmpImage:=nil;
  ship.FGraphName:=ship.FGraphShip.TypeO;

end;


procedure SF_EquipmentImageName(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script EquipmentImageName');
  obj:=TObject(av[1].VDW);
  av[0].VStr:='';
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if(item <> nil) and (item is TEquipment) then
  begin
    av[0].VStr:=(item as TEquipment).FSysName;
    if (High(av) > 1) then (item as TEquipment).FSysName:=av[2].VStr;//example 'ArtTranclucator_' (CacheData, Bm.Items)
  end else if obj is TTranclucator then
  begin
    av[0].VStr:=(obj as TTranclucator).FArtSysName;
    if (High(av) > 1) then (obj as TTranclucator).FArtSysName:=av[2].VStr;
  end;
end;

procedure SF_StarFonImage(av:array of TVarEC; code:TCodeEC);
var
  star:TStar;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script StarFonImage');
  star:=TStar(av[1].VDW);
  av[0].VInt:=star.FFonImage;
  if (High(av) > 1) then star.FFonImage:=av[2].VInt;
end;



procedure SF_ExtremalTakeOff(av:array of TVarEC; code:TCodeEC);
begin
  GScriptTakeOff:=true;
end;

procedure SF_ForceNextDay(av:array of TVarEC; code:TCodeEC);
begin
  GScriptNextDay:=true;
end;

procedure SF_ScriptActionsRun(av:array of TVarEC; code:TCodeEC);
begin
  GScriptThread.Execute;
end;


procedure SF_StarListToPlanetList(av:array of TVarEC; code:TCodeEC);
var
  i,j,priority,cnt,dist: integer;
  value,visited_mult: double;
  star,star2: TStar;
  planet,planet2: TPlanet;
  racial_mult: array [Maloc..Gaal] of integer;
  element: Cardinal;
  pdbl: PDouble;
  li: TList;
begin
  if(High(av) < 6) then raise Exception.Create('Error.Script StarListToPlanetList');
  if(av[1].VType <> vtArray) then raise Exception.Create('Error.Script StarListToPlanetList - not array');

  if(High(av) > 6) and (av[7].VType <> vtArray) then raise Exception.Create('Error.Script StarListToPlanetList - not array');
  visited_mult:=0;
  if(High(av) > 7) then visited_mult:=av[8].VInt/100;

  racial_mult[Maloc]:=av[2].VInt;
  racial_mult[Peleng]:=av[3].VInt;
  racial_mult[People]:=av[4].VInt;
  racial_mult[Fei]:=av[5].VInt;
  racial_mult[Gaal]:=av[6].VInt;

  cnt:=av[1].VArray.Count;
  for i:=cnt-1 downto 0 do begin
    star:=TStar(av[1].VArray.Items[i].VDW);
    priority:=0;
    planet2:=nil;
    for j:=0 to star.FPlanets.Count-1 do begin
      planet:=star.FPlanets.Items[j];
      if planet.FOwner in [Maloc..Gaal] then begin
        if(priority < racial_mult[planet.FOwner]) then begin
          planet2:=planet;
          priority:=racial_mult[planet.FOwner];
        end;
      end;
    end;
    if(priority > 0) then av[1].VArray.Items[i].VDW:=Cardinal(planet2) else av[1].VArray.Del(i);
  end;
  cnt:=av[1].VArray.Count;
  if cnt>0 then begin
    li:=TList.Create;

    for i:=0 to cnt-1 do begin
      planet:=TPlanet(av[1].VArray.Items[i].VDW);
      star:=planet.FStar;
      j:=0;
      while (j < Galaxy.FStars.Count) and ((star.FStarDist[j].FStar as TStar).FStatus.Owners <> Klings) and ((star.FStarDist[j].FStar as TStar).FStatus.CustomFaction='') do j:=j+1;
      if(j = Galaxy.FStars.Count) then dist:=1 else dist:=star.FStarDist[j].FDist;
      value:=racial_mult[planet.FOwner]*dist;
      if (High(av) > 6) then
         for j:=0 to av[7].VArray.Count-1 do
           if(av[7].VArray.Items[j].VDW=Cardinal(star)) or (av[7].VArray.Items[j].VDW=star.FId) then value:=value * visited_mult;
      new(pdbl);
      pdbl^:=value;
      li.Add(pdbl);
    end;

    for i:=1 to cnt-1 do begin
      for j:=cnt-1 downto i do begin
        if(PDouble(li.Items[j])^ > PDouble(li.Items[j-1])^) then begin
          element:=Cardinal(av[1].VArray.Items[j]);
          av[1].VArray.Items[j]:=av[1].VArray.Items[j-1];
          av[1].VArray.Items[j-1]:=TVarEC(element);
          value:=PDouble(li.Items[j])^;
          PDouble(li.Items[j])^:=PDouble(li.Items[j-1])^;
          PDouble(li.Items[j-1])^:=value;
        end;
      end;
    end;
    li.Free;
  end;
  av[0].VInt:=cnt;
  if(cnt = 0) then av[1].VArray.Add(TVarEC.Create(vtUnknown));
end;


procedure SF_EndGame(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) > 0) then
  begin
	 GEndType:=av[1].VInt;
   GFormNext:=mlf_GameEnd;
   TMessageLoopGI(GForm[GFormCur]).ExitLoop();
  end else begin
   GFormScore.ScoreUpdateFromCurGame(Player<>nil);
   GFormAbout.FScore:=true;
   GFormNext:=mlf_About;
   TMessageLoopGI(GForm[GFormCur]).ExitLoop();
  end;
end;

procedure SF_CustomWin(av:array of TVarEC; code:TCodeEC);
var
  gevent:TGalaxyEvent;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script CustomWin');
  gevent := NewEvent('CustomWin');
  gevent.Add(av[1].VStr);//text
  if High(av) > 1 then gevent.Add(av[2].VInt) else gevent.Add(0);//custom screen num
//if special screen needed
//put it in Main.dat ML.GameEnd.Panel as Image with name 'CustomEndN' (where N=num, starting from 1, no missing numbers allowed)

  GEndType:=0;
  GFormNext:=mlf_GameEnd;
  TMessageLoopGI(GForm[GFormCur]).ExitLoop();
end;

procedure SF_CustomLose(av:array of TVarEC; code:TCodeEC);
var
  gevent:TGalaxyEvent;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script CustomLose');
  gevent := NewEvent('CustomLose');
  gevent.Add(av[1].VStr);
  if High(av) > 1 then gevent.Add(av[2].VInt) else gevent.Add(0);//custom screen num

  GEndType:=0;
  GFormNext:=mlf_GameEnd;
  TMessageLoopGI(GForm[GFormCur]).ExitLoop();
end;

procedure SF_PirateWin(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=Galaxy.FPirateWinType;
  if(High(av) > 0) then
   if(av[1].VInt >= 1) and (av[1].VInt <= 5) then begin
     Galaxy.FPirateTurnWin:=Galaxy.FTurn;
     Galaxy.FPirateWinType:=av[1].VInt;
   end;
end;


procedure SF_StartVideo(av:array of TVarEC; code:TCodeEC);
var req:PScriptVDRequest;
begin
  if (High(av) = 0) then begin av[0].VInt:=GScriptsThatCalledVD.Count; exit; end;

  if(High(av) < 2) then raise Exception.Create('Error.Script StartVideo');
  if GetCurrentML = GFormShip then
  begin
    GFormShip.FSoundLoop.SetVolume(0.0);

    with GFormShip.GetByName('Film') as TxvidGI do
    begin
      Active := true;
      if not ImageOpen(av[1].VStr{'data\record.vdo'}) then
      begin
        GFormShip.Record_Cancel;
        Exit;
      end;
    end;

    if GMusic then
    begin
      GR_MC.StopFast;
      while GR_MC.IsPlayEx do
      begin
        Sleep(1);
      end;
    end;

    if GMusic then
    begin
      GR_MC.PlayEx(av[2].VStr{'Record'});
      while not GR_MC.IsPlayEx do
      begin
        Sleep(1);
      end;
    end;

    GFormShip.FRecord_BeginSound := timeGetTime();
    if GFormShip.FRecord_TimerSound <> 0 then
    begin
      GFormShip.MT_Delete(GFormShip.FRecord_TimerSound);
      GFormShip.FRecord_TimerSound := 0;
    end;
    GFormShip.FRecord_TimerSound := GFormShip.MT_Add(5, 5, GFormShip.Record_TimerSound);

  end else begin
    new(req);

    req.FVideo:=av[1].VStr;
    req.FSoundtrack:=av[2].VStr;
    req.FScript:=GScriptCur;
    GScriptsThatCalledVD.Add(req);

    if GScriptCur<>nil then GScriptCur.FCodeInit.LocalVar.GetVar('GVideoStatus').VInt:=1;
    GFormNext:=GFormCur;
    TMessageLoopGI(GForm[GFormCur]).ExitLoop();
  end;
end;

procedure SF_StartMusic(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script StartMusic');
  if not GMusic then exit;

  if GetCurrentML = GFormStarMap then GFormStarMap.FDoNotChangeMusicInBattle:=true;
  GR_MC.StopFast;
  while GR_MC.IsPlayEx do Sleep(1);

  GR_MC.PlayEx(av[1].VStr{'Record'});
end;

procedure SF_NoComeKlingToStar(av:array of TVarEC; code:TCodeEC);
var
  star: TStar;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script NoComeKlingToStar');

  star:=TStar(av[1].VDW);
  if(star <> nil) then begin
    if star.FFlag_NoComeKling then av[0].VInt:=1 else av[0].VInt:=0;
    if(High(av) > 1) then star.FFlag_NoComeKling:=(av[2].VInt <> 0);
  end;
end;

procedure SF_NoDropToShip(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script NoDropToShip');

  ship:=TShip(av[1].VDW);
  if(ship <> nil) then begin
    if ship.FFlag_NoDrop then av[0].VInt:=1 else av[0].VInt:=0;
    if(High(av) > 1) then ship.FFlag_NoDrop:=(av[2].VInt <> 0);
  end;
end;

procedure SF_NoTargetToShip(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script NoTargetToShip');

  ship:=TShip(av[1].VDW);
  if(ship <> nil) then begin
    av[0].VInt:=integer(ship.FFlag_NoTarget);
    if(High(av) > 1) then ship.FFlag_NoTarget:=TTargeting(av[2].VInt);
  end;
  //0 - normal,
  //1 - no attack (except between hostile factions), 2 - no attack from AI including assists,
  //3 - no robbing from pirates and rangers, 4 - no robbing from rangers, 5 - no robbing from pirates
  //6 - attract pirates and ranger-pirates
end;

procedure SF_NoTalkToShip(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if High(av) < 1 then //raise Exception.Create('Error.Script NoTalkToShip');
  begin
    av[0].VInt:=ord(Player.FTalkLocked);
    exit;
  end;

  if (High(av) = 1) and ((av[1].VType<>vtDW) or (av[1].VDW < 255)) then
  begin
    av[0].VInt:=ord(Player.FTalkLocked);
    Player.FTalkLocked := (av[1].VInt<>0);
    exit;
  end;

  ship:=TShip(av[1].VDW);
  if(ship <> nil) then begin
    if ship.FFlag_NoTalk then av[0].VInt:=1 else av[0].VInt:=0;
    if(High(av) > 1) then ship.FFlag_NoTalk:=(av[2].VInt <> 0);
  end;
end;

procedure SF_NoScanToShip(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then //raise Exception.Create('Error.Script NoScanToShip');
  begin
    av[0].VInt:=ord(Player.FScanLocked);
    exit;
  end;

  if (High(av) = 1) and ((av[1].VType<>vtDW) or (av[1].VDW < 255)) then
  begin
    av[0].VInt:=ord(Player.FScanLocked);
    Player.FScanLocked := (av[1].VInt<>0);
    exit;
  end;

  ship:=TShip(av[1].VDW);
  if(ship <> nil) then begin
    if ship.FFlag_NoScan then av[0].VInt:=1 else av[0].VInt:=0;
    if(High(av) > 1) then ship.FFlag_NoScan:=(av[2].VInt <> 0);
  end;
end;


procedure SF_NoJump(av:array of TVarEC; code:TCodeEC);
begin
  if Player.FFlag_NoJump then av[0].VInt:=1 else av[0].VInt:=0;
  if(High(av) > 0) then Player.FFlag_NoJump:=(av[1].VInt <> 0);
end;

procedure SF_NoLanding(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script NoLanding');

  av[0].VInt:=0;
  obj:=TObject(av[1].VDW);
  if(obj is TPlanet) then begin
    if (obj as TPlanet).FFlag_NoLanding then av[0].VInt:=1;
    if(High(av) > 1) then (obj as TPlanet).FFlag_NoLanding:=(av[2].VInt <> 0);

  end else if(obj is TRuins) then begin
    if (obj as TRuins).FFlag_NoLanding then av[0].VInt:=1;
    if(High(av) > 1) then (obj as TRuins).FFlag_NoLanding:=(av[2].VInt <> 0);
  end;
end;

procedure SF_NoShopUpdate(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script NoShopUpdate');

  av[0].VInt:=0;
  obj:=TObject(av[1].VDW);
  if(obj is TPlanet) then begin
    av[0].VInt:=(obj as TPlanet).FFlag_NoShopUpdate;
    if(High(av) > 1) then (obj as TPlanet).FFlag_NoShopUpdate:=av[2].VInt;

  end else if(obj is TRuins) then begin
    av[0].VInt:=(obj as TRuins).FFlag_NoShopUpdate;
    if(High(av) > 1) then (obj as TRuins).FFlag_NoShopUpdate:=av[2].VInt;
  end;
  //0 - normal, 1 - no shop update, 2 - no goods update only, 3 - no eq update only
end;


procedure SF_NoDropItem(av:array of TVarEC; code:TCodeEC);
var
  obj:TObject;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script NoDropItem');

  av[0].VInt:=0;
  item:=nil;
  obj:=TObject(av[1].VDW);
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;

  if(item <> nil) then
  begin
    if item.FFlag_NoDrop then av[0].VInt:=1;
    if(High(av) > 1) then item.FFlag_NoDrop:=(av[2].VInt <> 0);
  end;
end;

procedure SF_CanSellItem(av:array of TVarEC; code:TCodeEC);
var
  obj:TObject;
  sitem: TScriptItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script CanSellItem');

  av[0].VInt:=1;
  sitem:=nil;
  obj:=TObject(av[1].VDW);
  if(obj is TItem) then sitem:=TScriptItem(TItem(obj).FScriptItem);
  if(obj is TScriptItem) then sitem:=TScriptItem(obj);

  if(sitem <> nil) then
  begin
    if not sitem.FFlag_CanSell then av[0].VInt:=0;
    if High(av) > 1 then sitem.FFlag_CanSell:=(av[2].VInt <> 0);
  end;
end;


procedure SF_TruceBetweenShips(av:array of TVarEC; code:TCodeEC);
var
  ship1,ship2: TShip;
  boss1,boss2: TShip;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script TruceBetweenShips');
  ship1:=TShip(av[1].VDW);
  ship2:=TShip(av[2].VDW);
  if(ship1 <> nil) and (ship2 <> nil) then
  begin
    boss1:=ship1.FShipPartner;
    boss2:=ship2.FShipPartner;

    if (boss1<>nil) and (boss2<>nil) then
      if (boss1.FShipBad=boss2) or (boss2.FShipBad=boss1) then
        boss1.TruceWithShip(boss2);

    if boss1<>nil then
      if (boss1.FShipBad=ship2) or (ship2.FShipBad=boss1) then
        boss1.TruceWithShip(ship2);

    if boss2<>nil then
      if (ship1.FShipBad=boss2) or (boss2.FShipBad=ship1) then
        ship1.TruceWithShip(boss2);

    ship1.TruceWithShip(ship2);
  end;
end;


procedure SF_ShipInPrison(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipInPrison');

  av[0].VInt:=0;
  ship:=TShip(av[1].VDW);
  if ship.FCurPlanet<>nil then
  begin
    if ship=Player then
    begin
      if Player.FPrison then av[0].VInt:=1;
      exit;
    end;
    case ship.FShipType of
      t_Ranger: begin
        av[0].VInt:=(ship as TRanger).FPrison;
        if(High(av) > 1) then (ship as TRanger).FPrison:=av[2].VInt;
      end;
      t_Pirate: begin
        av[0].VInt:=(ship as TPirate).FPrison;
        if(High(av) > 1) then (ship as TPirate).FPrison:=av[2].VInt;
      end;
    end;
  end;
end;


procedure SF_ShipPartners(av:array of TVarEC; code:TCodeEC);
var
  ship,ranger: TShip;
  i,num,counter: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipPartners');
  ship:=TShip(av[1].VDW);
  num:=-1;
  counter:=-1;
  av[0].VDW:=0;
  if(High(av) > 1) then num:=av[2].VInt;
  for i:=0 to Galaxy.FRangers.Count-1 do begin
    ranger:=Galaxy.FRangers.Items[i];
    if(ranger.FShipPartner=ship) then begin
      counter:=counter + 1;
      if(counter = num) then begin
        av[0].VDW:=Cardinal(ranger);
        exit;
      end;
    end;
  end;
  if(High(av) = 1) then av[0].VInt:=counter + 1;
end;

procedure SF_PlayerPirates(av:array of TVarEC; code:TCodeEC);
var
  no,cnt: integer;
begin
  if Player.FPirates = nil then cnt:=0
  else cnt:=Player.FPirates.Count;

  if(High(av) < 1) then
  begin
    av[0].VInt:=cnt;
    exit;
  end;

  no:=av[1].VInt;
  if (no<0) or (no>=cnt) then
  begin
    av[0].VDW:=0;
    exit;
  end;

  av[0].VDW:=Cardinal(Player.FPirates.Items[no]);

end;


procedure SF_ShipIsPartner(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipIsPartner');
  ship:=TShip(av[1].VDW);
  if(ship <> nil) then av[0].VDW:=Cardinal(ship.FShipPartner);
end;


procedure SF_ShipFreeSpace(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if High(av)<>1 then raise Exception.Create('Error.Script ShipFreeSpace');
  ship:=TShip(av[1].VDW);
  if(ship <> nil) then av[0].VInt:=ship.FFreeSpace;
end;


procedure SF_ShipWealth(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if High(av)<>1 then raise Exception.Create('Error.Script ShipWealth');
  ship:=TShip(av[1].VDW);
  if(ship <> nil) then av[0].VInt:=ship.FCapital;
end;


procedure SF_DomiksDefeated(av:array of TVarEC; code:TCodeEC);
var ser:TDominatorSeries;
begin
  if High(av)<1 then
  begin
    if not Galaxy.DominatorBossInWar then av[0].VInt:=1 else av[0].VInt:=0;
    exit;
  end;

  ser:=TDominatorSeries(av[1].VInt);

  case ser of
    t_Blazer:
    begin
      if Galaxy.FBlazerTurnWin = 0 then av[0].VInt:=0
      else if (Galaxy.FBlazerLanding<>0) and (Blazer<>nil) then av[0].VInt:=3
      else if Galaxy.FBlazerSelfDestruction<>0 then av[0].VInt:=2
      else av[0].VInt:=1;
    end;
    t_Keller:
    begin
      if Galaxy.FKellerTurnWin=0 then av[0].VInt:=0
      else if Galaxy.FKellerLeave<>0 then av[0].VInt:=2
      else if Galaxy.FKellerNewResearch<>0 then av[0].VInt:=3
      else av[0].VInt:=1;
    end;
    t_Terron:
    begin
      if Galaxy.FTerronTurnWin=0 then av[0].VInt:=0
      else if Galaxy.FTerronToStar<>0 then av[0].VInt:=2
      else if Galaxy.FTerronLandingLockTurn<>0 then av[0].VInt:=3
      else av[0].VInt:=1;
    end;
    else av[0].VInt:=0;
  end;
end;

procedure SF_CoalitionDefeated(av:array of TVarEC; code:TCodeEC);
begin
  if(Galaxy.FCoalitionDefeatedTurn<>0) then av[0].VInt:=1 else av[0].VInt:=0;
  if High(av)>0 then
  begin
    if av[1].VInt = 1 then Galaxy.FCoalitionDefeatedTurn:=Galaxy.FTurn
    else Galaxy.FCoalitionDefeatedTurn:=0;
  end;
end;


procedure SF_ShipRefuel(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipRefuel');
  ship:=TShip(av[1].VDW);
  if(ship <> nil) and (ship.FFuelTanks <> nil) then ship.FFuelTanks.FFuel:=ship.FFuelTanks.FCapacity;
end;


procedure SF_ShipRepairEq(av:array of TVarEC; code:TCodeEC);
var
  i: Integer;
  eq: TEquipment;
  a: TArtefact;
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipRepairEq');
  ship:=TShip(av[1].VDW);
  for i:=ship.FEquipments.Count-1 downto 0 do begin
    eq:=ship.FEquipments.Items[i];
    if eq.FExplotable then eq.RestoreDuration;
  end;
  for i:=0 to ship.FArtefacts.Count-1 do begin
    a:=ship.FArtefacts.Items[i];
    if a.FExplotable then a.RestoreDuration;
  end;
end;


procedure SF_ItemInScript(av:array of TVarEC; code:TCodeEC);
var
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemInScript');
  item:=TItem(av[1].VDW);
  if(item <> nil) and (item.FScriptItem <> nil) then av[0].VInt:=1 else av[0].VInt:=0;
end;


procedure SF_FindPlanetByAdvancement(av:array of TVarEC; code:TCodeEC);
var
  maxtech,mintech,targettech,curtech,techpercent,i,j,value:integer;
  owner:TStarOwners;
  star:TStar;
  planet,curplanet:TPlanet;

  procedure CalcValue;
  var k:TInvention;
  begin
    value:=0;
    for k:=Low(k) to High(k) do value:=value+planet.FScn.mOpenInvention[k];
    for k:=Low(k) to TechLevel do value:=value+2*planet.FScn.mOpenInvention[k];
    value:=value+(planet.FScn.mOpenInvention[TechLevel])*8+
    (planet.FScn.mOpenInvention[HullAlloy])*4+
    (planet.FScn.mOpenInvention[RepairRobotType])*2;
  end;

begin
  if(High(av) < 1) then raise Exception.Create('Error.Script FindPlanetByAdvancement');
  owner:=Normals;
  if(High(av) > 1) then owner:=TStarOwners(av[2].VInt);
  techpercent:=max(min(av[1].VInt,100),0);
  maxtech:=0;
  mintech:=1000;

  for i:=0 to Galaxy.FStars.Count-1 do
  begin
    star:=Galaxy.FStars.Items[i];
    if (star.FStatus.Owners = owner) and (star.FStatus.CustomFaction='') then
    begin
      for j:=0 to star.FPlanets.Count-1 do
      begin
        planet:=star.FPlanets.Items[j];
        if planet.FOwner <> None then
        begin
          CalcValue;
          maxtech:=max(value,maxtech);
          mintech:=min(value,mintech);
        end;
      end;
    end;
  end;

  targettech:=mintech+Round(((maxtech-mintech)*techpercent)/100);
  curtech:=0;
  curplanet:=nil;
  for i:=0 to Galaxy.FStars.Count-1 do
  begin
    star:=Galaxy.FStars.Items[i];
    if (star.FStatus.Owners = owner) and (star.FStatus.CustomFaction='') then
    begin
      for j:=0 to star.FPlanets.Count-1 do
      begin
        planet:=star.FPlanets.Items[j];
        if planet.FOwner <> None then
        begin
          CalcValue;
          if(curplanet=nil) or (Abs(value-targettech)<curtech) then
          begin
            curplanet:=planet;
            curtech:=Abs(value-targettech);
          end;
        end;
      end;
    end;
  end;
  av[0].VDW:=Cardinal(curplanet);
end;


procedure SF_StarListToTransitPlanetList(av:array of TVarEC; code:TCodeEC);
var
  i,j,k,priority,cnt,distance,distextra,extradistmax,corr_dist: integer;
  value,value2,visited_mult: double;
  star,star2,starfrom,starto: TStar;
  planet,planet2: TPlanet;
  racial_mult: array [0..4] of integer;
  element: Cardinal;
  pdbl: PDouble;
  li: TList;
begin
  if(High(av) < 4) then raise Exception.Create('Error.Script StarListToTransitPlanetList');

  corr_dist:=10;
  starfrom:=TStar(av[2].VDW);
  starto:=TStar(av[3].VDW);
  extradistmax:=av[4].VInt+corr_dist;
  distance:=Round(Dist(starfrom.FPos,starto.FPos));
  if(av[1].VType <> vtArray) then raise Exception.Create('Error.Script StarListToTransitPlanetList - not array');

  if(High(av) > 8) then begin
    for i:=0 to 4 do racial_mult[i]:=av[i+5].VInt;
  end else begin
    for i:=0 to 4 do racial_mult[i]:=100;
  end;

  if(High(av) > 10) then begin
    if(av[10].VType <> vtArray) then raise Exception.Create('Error.Script StarListToTransitPlanetList - not array2');
  end;
  visited_mult:=0;
  if(High(av) > 10) then visited_mult:=av[11].VInt/100;


  li:=TList.Create;
  i:=0;
  while(i < av[1].VArray.Count) do begin
    star:=TStar(av[1].VArray.Items[i].VDW);
    distextra:=Round(Dist(star.FPos,starto.FPos))+Round(Dist(star.FPos,starfrom.FPos))-distance+corr_dist;
    priority:=0;
    planet2:=nil;
    value2:=0;
    for j:=0 to star.FPlanets.Count-1 do begin
      planet:=star.FPlanets.Items[j];
      if(integer(planet.FOwner) < 5) then begin
        value:=racial_mult[integer(planet.FOwner)]*distextra/100;
        if(High(av) > 10) then begin
          for k:=0 to av[10].VArray.Count-1 do begin
            if(av[10].VArray.Items[k].VDW=Cardinal(planet)) or (av[10].VArray.Items[k].VDW=Cardinal(planet.FId)) then value:=value*visited_mult;
          end;
        end;
        if((planet2=nil) and (value<=extradistmax) and (value>0)) or ((value<value2) and (value>0)) then begin
          planet2:=planet;
          value2:=value;
        end;
      end;
    end;
    if(star=starfrom) or (star=starto) or (planet2=nil) then av[1].VArray.Del(i) else begin
      av[1].VArray.Items[i].VDW:=Cardinal(planet2);
      new(pdbl);
      pdbl^:=value2;
      li.Add(pdbl);
      i:=i+1;
    end;
  end;

  cnt:=av[1].VArray.Count;
  if cnt>0 then begin
    for i:=1 to cnt-1 do begin
      for j:=cnt-1 downto i do begin
        if(PDouble(li.Items[j])^ < PDouble(li.Items[j-1])^) then begin
          element:=Cardinal(av[1].VArray.Items[j]);
          av[1].VArray.Items[j]:=av[1].VArray.Items[j-1];
          av[1].VArray.Items[j-1]:=TVarEC(element);
          value:=PDouble(li.Items[j])^;
          PDouble(li.Items[j])^:=PDouble(li.Items[j-1])^;
          PDouble(li.Items[j-1])^:=value;
        end;
      end;
    end;
    li.Free;
  end;

  av[0].VInt:=cnt;
  if(cnt = 0) then av[1].VArray.Add(TVarEC.Create(vtUnknown));
end;


procedure SF_GalaxyEvents(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=Galaxy.FEvents.Count;
end;


procedure SF_GalaxyEventDate(av:array of TVarEC; code:TCodeEC);
var
  no: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script GalaxyEventDate');
  av[0].VInt:=0;
  no:=av[1].VInt;
  if(no >= 0) and (no < Galaxy.FEvents.Count) then av[0].VInt:=TGalaxyEvent(Galaxy.FEvents.Items[no]).FTurn;
end;


procedure SF_GalaxyEventType(av:array of TVarEC; code:TCodeEC);
var
  no: integer;
begin
  if High(av)<1 then raise Exception.Create('Error.Script GalaxyEventType');
  av[0].VStr:='';
  no:=av[1].VInt;
  if(no >= 0) and (no < Galaxy.FEvents.Count) then av[0].VStr:=TGalaxyEvent(Galaxy.FEvents.Items[no]).FType;
end;


procedure SF_GalaxyEventData(av:array of TVarEC; code:TCodeEC);
var
  no: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script GalaxyEventData');
  av[0].VInt:=0;
  no:=av[1].VInt;
  if(no >= 0) and (no < Galaxy.FEvents.Count) then begin
    if(High(av) > 1) then av[0].VInt:=TGalaxyEvent(Galaxy.FEvents.Items[no]).GetData(av[2].Vint)
    else av[0].VInt:=TGalaxyEvent(Galaxy.FEvents.Items[no]).FDataList.Count;
  end;
end;

procedure SF_GalaxyEventsTextData(av:array of TVarEC; code:TCodeEC);
var
  no:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script GalaxyEventTextData');
  no:=av[1].VInt;
  if(no >= 0) and (no < Galaxy.FEvents.Count) then begin
    if High(av)>1 then av[0].VStr:=TGalaxyEvent(Galaxy.FEvents.Items[no]).GetTextData(av[2].Vint)
    else av[0].VInt:=TGalaxyEvent(Galaxy.FEvents.Items[no]).FTextDataList.Count;
  end else av[0].VInt:=0;
end;


procedure SF_PlanetNews(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=Galaxy.FPlanetNews.Count;
end;

procedure SF_PlanetNewsDate(av:array of TVarEC; code:TCodeEC);
var
  no: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetNewsDate');
  av[0].VInt:=0;
  no:=av[1].VInt;
  if(no >= 0) and (no < Galaxy.FPlanetNews.Count) then av[0].VInt:=PPlanetNews(Galaxy.FPlanetNews.Items[no]).FDate;
end;

procedure SF_PlanetNewsType(av:array of TVarEC; code:TCodeEC);
var
  no: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetNewsType');
  av[0].VInt:=0;
  no:=av[1].VInt;
  if(no >= 0) and (no < Galaxy.FPlanetNews.Count) then av[0].VInt:=ord(PPlanetNews(Galaxy.FPlanetNews.Items[no]).FType);
end;
// starting from 0
{dsGalaxyNews, dsRevoltAnarchy,
    dsRevoltDictatorship, dsRevoltMonarchy, dsRevoltRepublic, dsRevoltDemocracy,
    dsMineralDeposit, dsNeedMineral, dsManyArms, dsNeedArms, dsManyTechnics,
    dsManyFood, dsNeedFood, dsManyMedicine, dsManyLuxury, dsNeedLuxury,
    dsManyAlcohol, dsNeedAlcohol,
    dsStarTransport, dsStarPiratesMany, dsStarPiratesSome, dsStarPiratesNone,
    dsStarRangers, dsStarBestRanger, dsStarKlingAttack, dsStarKlingLost,
    dsGroupWarriorLiberator, dsStarPiratesAttack, dsStarPiratesLost,
    dsStarNormalsCaptureKlings,dsStarNormalsCapturePirates,
    dsStarPiratesCaptureKlings,dsStarPiratesCaptureNormals,
    dsStarKlingsCaptureNormals,dsStarKlingsCapturePirates,
    dsCoalitionDefeated,dsNewBlackHole,
    dsEminentWarrior,dsEminentTrader,dsEminentPirate,dsRangerImprisoned,
    dsNewStation,dsInvestment,dsProgramResearched,dsSpecialShip,
    dsWBJumpPlanned}

procedure SF_PlanetNewsText(av:array of TVarEC; code:TCodeEC);
var
  no: integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PlanetNewsText');
  av[0].VStr:='';
  no:=av[1].VInt;
  if(no >= 0) and (no < Galaxy.FPlanetNews.Count) then
  begin
    av[0].VStr:=PPlanetNews(Galaxy.FPlanetNews.Items[no]).FText;
    if High(av) > 1 then PPlanetNews(Galaxy.FPlanetNews.Items[no]).FText := av[2].VStr;
  end;
end;


procedure SF_ControlledSystems(av:array of TVarEC; code:TCodeEC);
var
  i,sum:integer;
  owner: TStarOwners;
  star:TStar;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ControlledSystems');
  owner:=TStarOwners(av[1].VInt);
  sum:=0;
  for i:=0 to Galaxy.FStars.Count-1 do
  begin
    star:=Galaxy.FStars.Items[i];
    if star.FStatus.CustomFaction<>'' then continue;
    if star.FStatus.Owners = owner then sum:=sum+1;
  end;
  av[0].VInt:=sum;
end;


procedure SF_ShipInFear(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipInFear');
  ship:=TShip(av[1].VDW);
  if(ship <> nil) and ship.FFear then av[0].VInt:=1 else av[0].VInt:=0;
end;


procedure SF_CreateGoods(av:array of TVarEC; code:TCodeEC);
var
  goods:TGoods;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script CreateGoods');
  goods:=TGoods.Create;
  goods.Init(tItemType(av[1].VInt), av[2].VInt);
  av[0].VDW:=Cardinal(goods);
  if High(av) > 2 then goods.FNatural:=(av[3].VInt<>0);
end;


procedure SF_GetNodesFromShip(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
  i,nodestotake,shipnodes:integer;
  item:TItem;
  nodes:TProtoplasm;
  ser:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script GetNodesFromShip');
  ship:=TShip(av[1].VDW);
  nodestotake:=0;
  shipnodes:=0;
  ser:=-1;
  if(High(av) > 1) then nodestotake:=av[2].VInt;
  if(High(av) > 2) then ser:=av[3].VInt;
  for i:=ship.FEquipments.Count-1 downto 0 do begin
    item:=ship.FEquipments.Items[i];
    if item is TProtoplasm then begin
      nodes:=item as TProtoplasm;
      if (ser>=0) and (ser<>integer(nodes.FDS)) then continue;
      shipnodes:=shipnodes+nodes.FCount;
      if(nodestotake >= nodes.FCount) then begin
        nodestotake:=nodestotake-nodes.FCount;
        ship.FEquipments.Delete(i);
        nodes.Free;
      end else begin
        nodes.FCount:=nodes.FCount-nodestotake;
        nodes.FSize:=nodes.FCount;
        nodes.FCost:=ProtoplasmAverageCost*nodes.FCount;
        nodestotake:=0;
      end;
    end;
  end;

  if(High(av) > 1) and (av[2].VInt>0) then av[0].VInt:=nodestotake
  else av[0].VInt:=shipnodes;
end;

procedure SF_GetNodesFromStorage(av:array of TVarEC; code:TCodeEC);
var
  i,nodestotake,m:integer;
  su: PStorageUnit;
  nodes:TProtoplasm;
  obj:TObject;
  ser:integer;
begin

  obj:=nil;
  if (High(av)>=1) then obj:=TObject(av[1].VDW);
  av[0].VInt:=0;
  nodestotake:=0;
  ser:=-1;
  if (High(av)>1) then nodestotake:=av[2].VInt;
  if(High(av) > 2) then ser:=av[3].VInt;
  i:=0;

  while i < Player.FStorage.Count do
  begin
    su := Player.FStorage.Items[i];
    if ((su.FPlace = obj) or (obj = nil)) and (su.FItem.FItemType = t_Protoplasm) then
    begin
      nodes:=TProtoplasm(su.FItem);
      if (ser>=0) and (ser<>integer(nodes.FDS)) then continue;
      av[0].VInt:=av[0].VInt+nodes.FSize;
      if nodestotake<=0 then begin inc(i); continue; end;

      if nodestotake < nodes.FCount then
      begin
        m := nodes.FCount - nodestotake;
        nodes.FCost := Round(nodes.FCost / nodes.FCount * m);
        nodes.FCount := m;
        nodes.FSize := m;
        nodestotake := 0;
        inc(i);
      end
      else
      begin
        nodestotake := nodestotake - nodes.FSize;
        Player.FStorage.Delete(i);
        su.FItem.Free;
        Dispose(su);
      end;
    end
    else inc(i);
  end;


end;

procedure SF_RangerBaseNodes(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script RangerBaseNodes');
  av[0].VInt:=TRanger(av[1].VDW).FBaseNodCur;
  if(High(av) > 1) then TRanger(av[1].VDW).FBaseNodCur:=av[2].VInt;
end;


procedure SF_RuinsAllowModernization(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script RuinsAllowModernization');
  if TRuins(av[1].VDW).FSponsor then av[0].VInt:=1 else av[0].VInt:=0;
  if(High(av) > 1) then TRuins(av[1].VDW).FSponsor:=(av[2].VInt <> 0);
end;

procedure SF_RuinsMicromoduleChain(av:array of TVarEC; code:TCodeEC);
var obj:TObject;
    ruin:TRuins;
    chain,k:integer;
    altChain:boolean;
begin
  if (High(av) < 2) then raise Exception.Create('Error.Script RuinsMicromoduleChain');
  obj:=TObject(av[1].VDW);
  if not (obj is TRuins) then raise Exception.Create('Error.Script RuinsMicromoduleChain - not a ruins');
  ruin:=TRuins(obj);
  chain:=av[2].VInt;//0 - blue, 1 - yellow, 2 - red

  if (High(av) = 2) then
  begin
    for k:=0 to 50 do
    begin
      av[0].VInt:=ruin.GetMicromoduleChain(chain,k);
      if Player.MightNeedNodeNum(av[0].VInt+1) then break;
    end;
  end else begin
    k:=av[3].VInt;
    if High(av)>3 then altChain:=av[4].VInt<>0 else altChain:=false;//returns active or inactive chain (for current date)
    av[0].VInt:=ruin.GetMicromoduleChain(chain,k,altChain);
  end;
end;


procedure SF_DomikKilledInCurSystem(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then av[0].VInt:=Player.FKillInCurSystem[Klings]
  else av[0].VInt:=TNormalShip(av[1].VDW).FKillInCurSystem[Klings];
end;


procedure SF_ShipTypeN(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipTypeN');

  ship:=TShip(av[1].VDW);
  av[0].VInt:=integer(ship.FShipType);
end;

procedure SF_ShipSubType(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipSubType');

  ship:=TShip(av[1].VDW);
  if ship is TKling then av[0].VInt:=integer((ship as TKling).FType)
  else if ship is TTransport then av[0].VInt:=integer((ship as TTransport).FType)
  else if ship is TWarrior then av[0].VInt:=integer((ship as TWarrior).FWarriorType)
  else if ship is TPirate then av[0].VInt:=integer((ship as TPirate).FPirateType)
  else av[0].VInt:=0;

  if High(av) > 1 then
  begin
    if ship is TKling then TKling(ship).FType:=TKlingType(av[2].VInt)
    else if ship is TTransport then TTransport(ship).FType:=TTransportType(av[2].VInt)
    else if ship is TWarrior then TWarrior(ship).FWarriorType:=TWarriorType(av[2].VInt)
    else if ship is TPirate then TPirate(ship).FPirateType:=TPirateType(av[2].VInt);
  end;
end;


procedure SF_ShipChangeStar(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ShipChangeStar');

  if (TShip(av[1].VDW) = Player) and Player.InPlanetOrShip then
  begin
    ShopListToEquipmentShop;
    ShopListDestroy;
  end;

  TShip(av[1].VDW).ChangeStar(TSTar(av[2].VDW));
  if(TShip(av[1].VDW) = Player) then begin GCurStar:=Player.FCurStar; GCurStar.CalcDaySteps; end;
end;

procedure SF_IsFilm(av:array of TVarEC; code:TCodeEC);
begin
  if(GFormStarMap.FMode = fsmm_Film) then av[0].VInt:=1 else av[0].VInt:=0;
  Sleep(1);
end;


procedure SF_FilmFlags(av:array of TVarEC; code:TCodeEC);
var no:Cardinal;
    valI:integer;
    star:TStar;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script FilmFlags');

  if av[1].VDW<=3 then
  begin
    star:=GCurStar;
    no:=av[1].VDW;
    valI:=2;
  end else begin
    if High(av) < 2 then raise Exception.Create('Error.Script FilmFlags');
    star:=TStar(av[1].VDW);
    no:=av[2].VDW;
    valI:=3;
  end;

  case no of
    0:
    begin
      av[0].VInt:=ord(star.FFilmBuild);
    end;
    1:
    begin
      av[0].VInt:=ord(star.FWarPlayer);
      if High(av)>=valI then star.FWarPlayer:=(av[valI].VInt<>0);
    end;
    2:
    begin
      av[0].VInt:=ord(star.FBreakLongFly);
      if High(av)>=valI then star.FBreakLongFly:=(av[valI].VInt<>0);
    end;
    3:
    begin
      av[0].VInt:=ord(star.FDontStopFilm);
      if High(av)>=valI then star.FDontStopFilm:=(av[valI].VInt<>0);
    end;
  end;
end;
//usage
//FilmFlags(N)
//FilmFlags(N,val)
//FilmFlags(star,N)
//FilmFlags(star,N,val)

//N - flag type:
//0 FilmBuild, film is being made for this star, can't set value
//1 WarPlayer, set when something damages player or player damages other ships
//2 BreakLongFly, set when player picks up item, or forsaged engine's durability drops below threshold, or someone talks with player
//3 DontStopFilm, is never set by hardcode, can use to ignore interruptions and continue skipping turns until button is pressed
//values of all these flags are checked on turn's end and are reset when next turn starts

//star - no reason normally to set flags 1..3 for stars other than player's location, but can be used to skip checking



//for OnUse and OnAct code
procedure SF_ShowEffect(av:array of TVarEC; code:TCodeEC);
var
  lWeaponGraph:TWeaponSE;
  filmend_el:PEFilmEndUnit;
  targetSE,sourceSE:TObjectSE;
  targetFO,sourceFO:TEFilmObj;
  effName:WideString;
  target,source:TObject;
  item:TItem;
  damage,palette,expType:integer;
  explo,sound:boolean;
  color:Cardinal;
  lFilmObj: TEFilmObj;
  step:integer;
begin

  if(High(av) < 3) then raise Exception.Create('Error.Script ShowEffect');

  effName:=av[1].VStr;
  palette:=av[2].VInt;

  {
  'Weapon.Star'
  'Weapon.NoGraph'
  'Weapon.Asteroid'
  'Weapon.MissileHit'
  'Weapon.Shock'
  'Weapon.Nine'
  'Weapon.PDTurret'
  'Weapon.0' - 'Weapon.17'
  }

  //example
  //ShowEffect('Weapon.0',1,Player(),ShipStar(Player()),10,0,0,0,255,0);
  //shows weapon0 (laser) palette 1 shots Player from star, showing (not dealing) 10 damage,
  //without explosion, without sound, with numbers colored green (RGB=0,255,0)


  target:=TObject(av[3].VDW);
  source:=nil;
  if (High(av) > 3) then source:=TObject(av[4].VDW);

  damage:=0;
  if (High(av) > 4) then damage:=av[5].VInt;
  explo:=false;
  if (High(av) > 5) then explo:=av[6].VInt <> 0;
  sound:=true;
  if (High(av) > 6) then sound:=av[7].VInt <> 0;

  if (High(av) >= 10) then color:=GR_PF.Color(av[8].VInt, av[9].VInt, av[10].VInt)
  else begin
    if target is TShip then
    begin
      //color:=GR_PF.Color(255, 255, 255) //white
      if target=Player then color := OwnerColor(RaceToOwner(Player.FPilotRace))
      else if TShip(target).HasFactionEmblem then color := FactionColor(TScriptShip(TShip(target).FScriptShip).FCustomFaction)
      else color := OwnerColor(TShip(target).FOwner);
    end
    else color:=0;    //invisible (black)
  end;

  lWeaponGraph:=TWeaponSE.Create(effName,Point(0,0),palette);

  if (GCurStar<>nil) and GCurStar.FFilmBuild {and (CP_State=3)} then
  begin
    if GFilm = nil then exit;

    targetFO:=nil;
    if target is TShip then targetFO:=TShip(target).FFilmObj
    else if target is TPlanet then targetFO:=TPlanet(target).FFilmObj
    else if target is TStar then targetFO:=GFilm.ObjFind(ClassSEtoName(TStar(target).FGraphStar),TStar(target).FGraphStar.TypeO,TStar(target).FId)
    else if target is THole then targetFO:=THole(target).FFilmObj
    else if target is TMissile then targetFO:=TMissile(target).FFilmObj
    else if target is TAsteroid then targetFO:=TAsteroid(target).FFilmObj
    else begin
      item:=nil;
      if target is TItem then item:=target as TItem
      else if target is TScriptItem then item:=TScriptItem(target).FItem;
      if item<>nil then targetFO:=item.FFilmObj;
    end;

    sourceFO:=nil;
    if source<>nil then
    begin
      if source is TShip then sourceFO:=TShip(source).FFilmObj
      else if source is TPlanet then sourceFO:=TPlanet(source).FFilmObj
      else if source is TStar then sourceFO:=GFilm.ObjFind(ClassSEtoName(TStar(source).FGraphStar),TStar(source).FGraphStar.TypeO,TStar(source).FId)
      else if source is THole then sourceFO:=THole(source).FFilmObj
      else if source is TMissile then sourceFO:=TMissile(source).FFilmObj
      else if source is TAsteroid then sourceFO:=TAsteroid(source).FFilmObj
      else begin
        item:=nil;
        if source is TItem then item:=source as TItem
        else if source is TScriptItem then item:=TScriptItem(source).FItem;
        if item<>nil then sourceFO:=item.FFilmObj;
      end;
    end;

    step:=GCurStar.FCurStep;

    lFilmObj := GFilm.ObjAdd(0, lWeaponGraph, '', '');
    GFilm.OrderWeaponSetShip(step, lFilmObj, sourceFO, targetFO);
    GFilm.OrderWeaponSet(step, lFilmObj, color,damage,explo,sound);
    if explo and (av[6].VInt>1) then
    begin
      expType:=av[6].VInt-1;
      GFilm.OrderWeaponTypeExpl(step, lFilmObj, expType);
      if expType=SEWE_Kamikaze then GFilm.OrderTrans(step,targetFO,0);
    end;
    GFilm.OrderGraphConnect(step, lFilmObj);


  end else begin

    targetSE:=nil;
    if target is TShip then targetSE:=TShip(target).FGraphShip
    else if target is TPlanet then targetSE:=TPlanet(target).FGraphPlanet
    else if target is TStar then targetSE:=TStar(target).FGraphStar
    else if target is THole then targetSE:=THole(target).FGraphHole
    else if target is TMissile then targetSE:=TMissile(target).FGraph
    else if target is TAsteroid then targetSE:=TAsteroid(target).FGraph
    else begin
      item:=nil;
      if target is TItem then item:=target as TItem
      else if target is TScriptItem then item:=TScriptItem(target).FItem;
      if item<>nil then targetSE:=item.GraphItem;
    end;

    if targetSE = nil then exit;

    sourceSE:=nil;
    if source<>nil then
    begin
      if source is TShip then sourceSE:=TShip(source).FGraphShip
      else if source is TPlanet then sourceSE:=TPlanet(source).FGraphPlanet
      else if source is TStar then sourceSE:=TStar(source).FGraphStar
      else if source is THole then sourceSE:=THole(source).FGraphHole
      else if source is TMissile then sourceSE:=TMissile(source).FGraph
      else if source is TAsteroid then sourceSE:=TAsteroid(source).FGraph
      else begin
        item:=nil;
        if source is TItem then item:=source as TItem
        else if source is TScriptItem then item:=TScriptItem(source).FItem;
        if item<>nil then sourceSE:=item.GraphItem;
      end;
    end;

    lWeaponGraph.WeaponSetShip(sourceSE,targetSE);
    lWeaponGraph.WeaponSet(color,damage,explo,sound);


    if GetCurrentML = GFormStarMap then
    begin
      if GFilmEnd=nil then GFilmEnd:=TEFilmEnd.Create;
      filmend_el:=GFilmEnd.UnitAdd;

      LinkToSE(TObjectSE(filmend_el.FEvent),lWeaponGraph);
      LinkToSE(TObjectSE(filmend_el.FObj),nil);

      filmend_el.FEvent.Connect(GProcessSE.Space);
    end
    else
    GFormStarMap.FRequestedEffectsList.Add(lWeaponGraph);

  end;


end;
//ShowEffect( 'Weapon.13',0,ShipStar(Player()));
//ShowStaticEffect('TeleportIn',100,100);
procedure SF_ShowStaticEffect(av:array of TVarEC; code:TCodeEC);
var x,y:integer;
    eff:TGAIEffectSE;
    name:WideString;
    duration:single;
    lFilmObj: TEFilmObj;
    step:integer;
    filmend_el:PEFilmEndUnit;
begin
  if High(av) < 3 then raise Exception.Create('Error.Script ShowStaticEffect');
  name:=av[1].VStr;
  x:=av[2].VInt;
  y:=av[3].VInt;
  if High(av) > 3 then duration:=0.01*av[4].VInt else duration:=1.0;
  eff:=TGAIEffectSE.Create('Effect.'+name, Point(0, 0));

  if (GCurStar<>nil) and GCurStar.FFilmBuild {and (CP_State=3)} then
  begin
    if GFilm = nil then exit;
    step:=GCurStar.FCurStep;

    lFilmObj := GFilm.ObjAdd(0, eff, '', '');
    GFilm.OrderGAIEffectPos(step, lFilmObj, Point(x,y));
    GFilm.OrderGAIEffectDuration(step, lFilmObj, duration);
    GFilm.OrderGraphConnect(step, lFilmObj);

  end else begin

    eff.SetPosition(Point(x,y));
    eff.SetDuration(duration);


    if GetCurrentML = GFormStarMap then
    begin
      if GFilmEnd=nil then GFilmEnd:=TEFilmEnd.Create;
      filmend_el:=GFilmEnd.UnitAdd;

      LinkToSE(TObjectSE(filmend_el.FEvent),eff);
      LinkToSE(TObjectSE(filmend_el.FObj),nil);

      filmend_el.FEvent.Connect(GProcessSE.Space);
    end
    else
    GFormStarMap.FRequestedEffectsList.Add(eff);

  end;
end;

//for OnUse and OnAct code
procedure SF_FilmSound(av:array of TVarEC; code:TCodeEC);
var
  targetFO:TEFilmObj;
  soundName:WideString;
  target:TObject;
  item:TItem;
  step:integer;
begin

  if(High(av) < 2) then raise Exception.Create('Error.Script FilmSound');

  soundName:=av[1].VStr;
  target:=TObject(av[2].VDW);

  if (GCurStar<>nil) and GCurStar.FFilmBuild {and (CP_State=3)} then
  begin
    if GFilm = nil then exit;

    targetFO:=nil;
    if target is TShip then targetFO:=TShip(target).FFilmObj
    else if target is TPlanet then targetFO:=TPlanet(target).FFilmObj
    else if target is TStar then targetFO:=GFilm.ObjFind(ClassSEtoName(TStar(target).FGraphStar),TStar(target).FGraphStar.TypeO,TStar(target).FId)
    else if target is THole then targetFO:=THole(target).FFilmObj
    else if target is TMissile then targetFO:=TMissile(target).FFilmObj
    else if target is TAsteroid then targetFO:=TAsteroid(target).FFilmObj
    else begin
      item:=nil;
      if target is TItem then item:=target as TItem
      else if target is TScriptItem then item:=TScriptItem(target).FItem;
      if item<>nil then targetFO:=item.FFilmObj;
    end;

    step:=GCurStar.FCurStep;
    GFilm.OrderSound(step,targetFO,soundName);

  end else GR_SC.Play(soundName);

end;

procedure SF_FireWeapon(av:array of TVarEC; code:TCodeEC); //with all visual effects, no range check
var
  desobj:TObject;
  souship:TShip;
  weap:TWeapon;
  ffilm:boolean;
begin
  if(High(av) < 3) then raise Exception.Create('Error.Script FireWeapon');
  souship:=TShip(av[1].VDW);
  desobj:=TObject(av[2].VDW);
  weap:=TWeapon(av[3].VDW);
  ffilm:=souship.FCurStar.FFilmBuild;

  if (desobj is TMissile) then souShip.FireWeaponAtMissile(weap,desobj,ffilm)
  else if (desobj is TShip) then souShip.FireWeaponAtShip(weap,TShip(desobj),ffilm)
  else if (desobj is TItem) then souShip.FireWeaponAtItem(weap,TItem(desobj),ffilm) //weapon can be 0 here
  else if (desobj is TAsteroid) then souShip.FireWeaponAtAsteroid(weap,desobj,ffilm);

end;

procedure SF_WeaponHit(av:array of TVarEC; code:TCodeEC); //no visual effects here
var
  desobj:TObject;
  souship:TShip;
  weap:TWeapon;
  range:integer;
  color:Cardinal;
  zok:boolean;
  mi:TMissile;
  star:TStar;
  dt:TSetDamageType;
begin
  if(High(av) < 3) then raise Exception.Create('Error.Script WeaponHit');
  souship:=TShip(av[1].VDW);
  desobj:=TObject(av[2].VDW);
  weap:=TWeapon(av[3].VDW);

  range:=-1;
  if High(av) > 3 then range:=av[4].VInt;

  if desobj is TShip then av[0].VInt := TShip(desobj).WeaponHit(souship, weap, range, color,dt)  //returns damage
  else if desobj is TMissile then
  begin
    mi:=TMissile(desobj);
    zok:=mi.Hit(souship, weap);
    zok:=souship.ScriptItemsAct(t_OnWeaponShot,mi,weap,ord(zok))<>0;
    if zok then
    begin
      star:=mi.FStar;
      if star.FFilmBuild then
      begin
        GFilm.OrderGraphDisconnect(star.FCurStep, mi.FFilmObj);
        star.FDestroyObjEndFilm.Add(mi.FFilmObj);
        DetachFromSE(TObjectSE(mi.FGraph));
      end;
      mi.Free;
    end;
    av[0].VInt := ord(zok);      //returns flag hit/miss
  end;

end;

procedure SF_DealDamageToShip(av:array of TVarEC; code:TCodeEC); //no visual effects here
var
  desobj:TObject;
  souship,desship:TShip;
  damage:integer;
  damageset:TSetDamageType;
  range:integer;
  color:Cardinal;
begin
  if(High(av) < 4) then raise Exception.Create('Error.Script DealDamageToShip');
  desship:=TShip(av[1].VDW);
  souship:=TShip(av[2].VDW);//can be 0
  damage:=av[3].VInt;
  damageset:=TSetDamageType(Cardinal(av[4].VDW));

  range:=-1;
  if High(av) > 4 then range:=av[5].VInt;


  //warning! this will generate t_OnDealingDamage event for souship and t_OnTakingDamage for desship with potential execution of actcode as an interrupt
  av[0].VInt := desship.Hit(souship,damage,range,color,damageset);

end;



procedure SF_LaunchMissile(av:array of TVarEC; code:TCodeEC);
var
  desobj,item:TObject;
  souship:TShip;
  weap:TWeapon;
  t:integer;
  mi:TMissile;
  step:integer;
begin
  if(High(av) < 3) then raise Exception.Create('Error.Script LaunchMissile');
  souship:=TShip(av[1].VDW);
  desobj:=TObject(av[2].VDW);
  item:=TObject(av[3].VDW);

  if item is TScriptItem then weap:=TWeapon(TScriptItem(item).FItem)
  else weap:=TWeapon(item);

  t:=0; //starting position of missile, 0 - center
  if High(av) > 3 then t:=av[4].VInt;

  if weap is TCustomWeapon then
  begin
    mi:=TCustomMissile.Create;
    TCustomMissile(mi).InitC(souship.FCurStar,souship,TCustomWeapon(weap),desobj,t);
  end else begin
    mi := TMissile.Create;
    mi.Init(souship.FCurStar,souship,weap,desobj,t);
  end;
  souship.ScriptItemsAct(t_OnMissileShot,mi,weap);

  av[0].VDW:=Cardinal(mi);

  if souship.FCurStar.FFilmBuild then
  begin
    step:=souship.FCurStar.FCurStep;

    mi.StepDayStart(step, true, true);

    GFilm.OrderGraphDisconnect(0, mi.FFilmObj);
  end;
end;

procedure SF_SpawnMissile(av:array of TVarEC; code:TCodeEC);
var
  star:TStar;
  desobj:TObject;
  x,y:integer;
  angle:single;
  minDam,maxDam:integer;
  speed:single;
  it:TItemType;
  bon,spec:integer;
  mi:TMissile;
  step:integer;
begin
  if(High(av) < 9) then raise Exception.Create('Error.Script SpawnMissile');
  star:=TStar(av[1].VDW);
  desobj:=TObject(av[2].VDW);
  x:=av[3].VInt;
  y:=av[4].VInt;
  angle:=av[5].VInt;
  minDam:=av[6].VInt;
  maxDam:=av[7].VInt;
  speed:=av[8].VInt;

  if High(av)>9 then
  begin
    bon:=av[10].VInt+1;
    spec:=av[11].VInt+1;
  end else begin
    bon:=0;
    spec:=0;
  end;

  if av[9].VType = vtStr then
  begin
    mi := TCustomMissile.Create;
    TCustomMissile(mi).InitCAlt(star,desobj,x,y,angle,minDam,maxDam,speed,av[9].VStr,bon,spec);
  end else begin
    it:=TItemType(av[9].VInt);
    mi := TMissile.Create;
    mi.InitAlt(star,desobj,x,y,angle,minDam,maxDam,speed,it,bon,spec);
  end;



  av[0].VDW:=Cardinal(mi);

  if star.FFilmBuild then
  begin
    step:=star.FCurStep;

    mi.StepDayStart(step, true, true);

    GFilm.OrderGraphDisconnect(0, mi.FFilmObj);
  end;
end;


procedure SF_BonusText(av:array of TVarEC; code:TCodeEC);
var
  no:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script BonusText');
  no:=av[1].VInt;
  if(no >= 0) and (no < GCntMicroModuls) then av[0].VStr:=MicroModuleText(no,clr)
  else av[0].VStr:='';
end;


procedure SF_PlanetPirateClan(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VDW:=Cardinal(Planet_PirateClan);
end;

procedure SF_Blazer(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VDW:=Cardinal(Blazer);
end;

procedure SF_Keller(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VDW:=Cardinal(Keller);
end;

procedure SF_Terron(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VDW:=Cardinal(Terron);
end;


procedure SF_PirateType(av:array of TVarEC; code:TCodeEC);
var
  ship: TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script PirateType');
  ship:=TShip(av[1].VDW);
  if (ship is TPirate)
    then av[0].VInt:=integer(TPirate(ship).FPirateType)
    else av[0].VInt:=0;
end;


procedure SF_PlayerQuestInProgress(av:array of TVarEC; code:TCodeEC);
var
 quest:PQuest;
 i:integer;
 pla:TPlanet;
begin
  if Player.FQuests<>nil then
  begin
    if High(av) > 0 then pla:=TPlanet(av[1].VDW) else pla:=nil;
    for i:=0 to Player.FQuests.Count-1 do
    begin
      quest:=Player.FQuests.Items[i];
      if (pla<>nil) and (quest.Planet <> pla) then continue;
      if not quest.Successful then begin av[0].VInt:=1; exit; end;
    end;
  end;
  av[0].VInt:=0;
end;

procedure SF_PlayerQuestsCompleted(av:array of TVarEC; code:TCodeEC);
var
 quest:^TPlayerOldQuest;
 i:integer;
begin
  av[0].VInt:=0;
  if (PlayerOldQuests<>nil) and (PlayerOldQuests.Count>0) then
  for i:=0 to PlayerOldQuests.Count-1 do
  begin
    quest:=PlayerOldQuests.Items[i];
    if(High(av) >= 1) and (quest.TypeQuest <> TTypeQuest(av[1].VInt)) then continue;
    //TTypeQuest = (SendLetter, KillShip, PlanetQuest, DefSystem, DefShip);
    if quest.Successful then av[0].VInt:=av[0].VInt+1;
  end;
end;

procedure SF_QuestsStatusByNom(av:array of TVarEC; code:TCodeEC);
var qtype:TTypeQuest;
    qnom,i:integer;
    oldquest:^TPlayerOldQuest;
    quest:PQuest;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script QuestsStatusByNom');
  qtype:=TTypeQuest(av[1].VInt);
  //TTypeQuest = (SendLetter, KillShip, PlanetQuest, DefSystem, DefShip);
  qnom:=av[2].VInt;

  if (PlayerOldQuests<>nil) and (PlayerOldQuests.Count>0) then
    for i:=0 to PlayerOldQuests.Count-1 do
    begin
      oldquest:=PlayerOldQuests.Items[i];
      if(oldquest.TypeQuest <> qtype) then continue;
      if(oldquest.QuestNumber <> qnom) then continue;
      if oldquest.Successful then av[0].VInt:=3 else av[0].VInt:=4;
      exit;
    end;

  if (Player.FQuests<>nil) and (Player.FQuests.Count>0) then
    for i:=0 to Player.FQuests.Count-1 do
    begin
      quest:=Player.FQuests.Items[i];
      if(quest.TypeQuest <> qtype) then continue;
      if(quest.QuestNumber <> qnom) then continue;
      if quest.Successful then av[0].VInt:=2 else av[0].VInt:=1;
      exit;
    end;

  av[0].VInt:=0;
  //0 - not taken, 1 - taken, 2 - completed, 3 - completed and got reward, 4 - failed
end;

procedure SF_PlayerPlanetaryBattlesCompleted(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=Player.FPlanetBattlesWin;
end;

procedure SF_PlayerMayTakeSubCrack(av:array of TVarEC; code:TCodeEC);
begin
  if Player.MayTakeSubCrack then av[0].VInt:=1 else av[0].VInt:=0;
end;

procedure SF_SubCrackCost(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=Player.SubCrackCost;
end;

procedure SF_ShipCalcParam(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipCalcParam');
  TShip(av[1].VDW).CalcParam();
end;

procedure SF_ShipRefit(av:array of TVarEC; code:TCodeEC);
var ship:TShip;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipRefit');
  av[0].VInt:=0;
  ship:=TShip(av[1].VDW);
  //if (ship.FCurPlanet=nil) and (ship.FCurShip=nil) then Exit;
  //if (ship.FCurShip<>nil) and not(ship.FCurShip is TRuins) then Exit;
  if (High(av) > 2) and (ship.SMoney<av[3].VInt) then ship.SMoney:=av[3].VInt;
  ship.Refit(true);
  if (High(av) > 1) then
    if ship.FHull.FSize<av[2].VInt then begin
    ship.FHull.FSize:=av[2].VInt;
    ship.FHull.FHitPoints:=av[2].VInt;
    end;
  ship.CalcParam();
  av[0].VInt:=1;
end;

procedure SF_ShipImproveItems(av:array of TVarEC; code:TCodeEC);
var ship:TShip;
 i,n:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipRefit');
  av[0].VInt:=0;
  ship:=TShip(av[1].VDW);
  n:=1;
  if(High(av) > 1) then n:=av[2].VInt;
  for i:=1 to n do ship.ImprovementItems;
  ship.CalcParam;
  if ship.FFreeSpace<ship.MustHaveFreeSpace then begin
    ship.FHull.FSize:=ship.FHull.FSize-ship.FFreeSpace+ship.MustHaveFreeSpace;
    if (ship.FCurPlanet<>nil) or (ship.FCurShip<>nil) then ship.FHull.FHitPoints:=ship.FHull.FSize;
    end;
  ship.CalcParam();
end;

procedure SF_ItemImprovement(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
  eq:TEquipment;
  tId:Cardinal;
  itype:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script SF_ItemImprovement');
  obj:=TObject(av[1].VDW);
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  av[0].VInt:=0;
  if not (item.FItemType in ShipEquipments) then Exit;
  eq:=TEquipment(item);
  if not eq.NormalCharacters then av[0].VInt:=1;

  if (High(av) > 1) then
  begin
    itype:=av[2].VInt;
    if (itype<ord(Low(TImprovementItem))) or (itype>ord(High(TImprovementItem))) then itype:=ord(AnyImprovement);
    if (High(av) > 2) then eq.FDetailImprovement:=av[3].VInt else eq.FDetailImprovement:=0;

    if High(av) > 3 then
    begin
      tId:=eq.FId;
      eq.FId:=av[4].VDW;
      eq.Improvement(TImprovementItem(itype));
      eq.FId:=tId;
    end
    else eq.Improvement(TImprovementItem(itype));
  end;
end;

procedure SF_ShipFreeFlight(av:array of TVarEC; code:TCodeEC);
var
  i:integer;
  ship,curship:TShip;
  curscript:TScript;
  sship:TScriptShip;
  cs:TVarEC;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script SF_ShipFreeFlight');
  ship:=TShip(av[1].VDW);


  if GScriptCur=nil then
  begin
    ship.NextDayLogic;
    exit;
  end;
  curscript:=GScriptCur;
  cs:=GScriptCur.FCodeInit.LocalVar.GetVar('CurShip');
  curship:=nil;

  for i:=0 to curscript.FShips.Count-1 do
  begin
    sship:=curscript.FShips.Items[i];
    if Cardinal(sship.FShip) <> cs.VDW then continue;
    curship:=TShip(cs.VDW);
    break;
  end;


  ship.NextDayLogic;

  if (curship<>nil) and (curship.FScriptShip<>nil) and (TScriptShip(curship.FScriptShip).FScript=curscript) then curscript.SetGlobal(TScriptShip(curship.FScriptShip))
  else begin
    GScriptCur:=curscript;
    cs.VDW:=Cardinal(curship);
    GScriptCur.FCurShip:=curship;
    if curship<>nil then GScriptCur.FCodeInit.LocalVar.GetVar('EndState').VInt:=0;
  end;
end;


procedure SF_ShipKillFactionInCurSystem(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SF_ShipKillFactionInCurSystem');
  ship:=TShip(av[1].VDW);
  if not (ship is TNormalShip) then
  begin
    av[0].VInt:=0;
    Exit;
  end;

  if av[2].VInt=-1 then
  begin
    av[0].VInt:=(ship as TNormalShip).FKillCustomInCurSystem;
    if High(av) > 2 then (ship as TNormalShip).FKillCustomInCurSystem:=av[3].VInt;
    exit;
  end;

  av[0].VInt:=(ship as TNormalShip).FKillInCurSystem[TStarOwners(av[2].VInt)];
  if High(av) > 2 then
  begin
    (ship as TNormalShip).FKillInCurSystem[TStarOwners(av[2].VInt)]:=av[3].VInt;
    ship.CalcStanding;
  end;
end;


procedure SF_CapitalShipStats(av:array of TVarEC; code:TCodeEC);
var
  obj:TObject;
  ship:TShip;
  hull:THull;
begin
  av[0].VInt:=0;
  if(High(av) < 1) then raise Exception.Create('Error.Script SF_CapitalShipStats');
  obj:=TObject(av[1].VDW);
  ship:=nil; hull:=nil;
  if obj is TScriptShip then ship:=(obj as TScriptShip).FShip;
  if obj is TShip then ship:=TShip(obj);
  if ship<>nil then hull:=ship.FHull;
  if obj is THull then hull:=THull(obj);
  if hull=nil then Exit;
  av[0].VInt:=hull.FCapitalShip;
  if (High(av) > 1) then
  begin
    hull.FCapitalShip:=byte(av[2].VInt);
    if hull.FCapitalShip = 1 then
    begin
      hull.FInterceptors:=true;
      if (High(av) > 2) then hull.FEnergyMax:=av[3].VInt else hull.FEnergyMax:=1000;
      hull.FEnergy:=min(hull.FEnergy,hull.FEnergyMax);
    end else begin
      hull.FInterceptors:=false;
      hull.FEnergyMax:=0;
      hull.FEnergy:=0;
    end;
  end;

  {if hull.FCapitalShip > 0 then av[0].VInt:=hull.FEnergyMax else av[0].VInt:=0;
  if (High(av) > 1) then
  begin
    hull.FCapitalShip:=byte(av[2].VInt);
    hull.FInterceptors:=(av[2].VInt = 0);
  end;
  if (High(av) > 2) then hull.FEnergyMax:=av[3].VInt;}
end;


procedure SF_PlayerBridge(av:array of TVarEC; code:TCodeEC);
var i:integer;
begin
  av[0].VInt:=Player.FCaptainOnTheBridge;

  if(High(av) > 0) then
  begin
    i:=av[1].VInt;
    if High(av) > 1 then Player.FBridgeBGReplace:=av[2].VStr else Player.FBridgeBGReplace:='';
    if i>0 then Player.GoToBridge(i) else Player.ExitBridge;
  end;
end;

procedure SF_PlayerDebt(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=Player.FDebt;
  if(High(av) > 0) then Player.FDebt:=av[1].VInt;
end;

procedure SF_PlayerDebtDate(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=Player.FDebtDate;
  if(High(av) > 0) then Player.FDebtDate:=av[1].VInt;
end;

procedure SF_PlayerDebtCnt(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=Player.FDebtCnt;
  if(High(av) > 0) then Player.FDebtCnt:=av[1].VInt;
end;

procedure SF_PlayerDeposit(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=Player.FDeposit;
  if(High(av) > 0) then Player.FDeposit:=av[1].VInt;
end;

procedure SF_PlayerDepositDate(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=Player.FDepositDate;
  if(High(av) > 0) then Player.FDepositDate:=av[1].VInt;
end;

procedure SF_PlayerDepositDay(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=Player.FDepositDay;
  if(High(av) > 0) then Player.FDepositDay:=av[1].VInt;
end;

procedure SF_PlayerDepositPercent(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=round(Player.FDepositPercent*100);
  if(High(av) > 0) then Player.FDepositPercent:=0.01*av[1].VInt;
end;

procedure SF_PlayerMedPolicy(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=Player.FMedPolicy;
  if(High(av) > 0) then Player.FMedPolicy:=av[1].VInt;
end;


procedure SF_ShipCustomShipInfosCount(av:array of TVarEC; code:TCodeEC);
var i,cnt:integer;
    ship:TShip;
    pa:PCustomShipInfo;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ShipCustomShipInfosCount');
  ship:=TShip(av[1].VDW);
  i:=0;cnt:=0;
  for i:=0 to ship.FCustomShipInfos.Count-1 do
  begin
    pa:=ship.FCustomShipInfos.Items[i];
    if not pa.Delete then inc(cnt);
  end;
  av[0].VInt:=cnt;
end;

procedure SF_ShipAddCustomShipInfo(av:array of TVarEC; code:TCodeEC);
var
  pa:PCustomShipInfo;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ShipAddCustomShipInfo');
  new(pa);
  TShip(av[1].VDW).FCustomShipInfos.Add(pa);
  pa.OnActCode:=nil;
  pa.InfoType:=av[2].VStr;
  pa.IsInit:=false;
  pa.Delete:=false;

  if (High(av) > 2) then pa.InfoDescription:=av[3].VStr else pa.InfoDescription:=''; //if desctiption is 'NoShow' info will not appear in list (but will still execute its code)

  if (High(av) > 3) then pa.InfoData1:=av[4].VInt else pa.InfoData1:=0;
  if (High(av) > 4) then pa.InfoData2:=av[5].VInt else pa.InfoData2:=0;
  if (High(av) > 5) then pa.InfoData3:=av[6].VInt else pa.InfoData3:=0;
  
  if (High(av) > 6) then pa.InfoTextData1:=av[7].VStr else pa.InfoTextData1:='';
  if (High(av) > 7) then pa.InfoTextData2:=av[8].VStr else pa.InfoTextData2:='';
  if (High(av) > 8) then pa.InfoTextData3:=av[9].VStr else pa.InfoTextData3:='';

  av[0].VDW:=Cardinal(pa);
end;

procedure SF_ShipDeleteCustomShipInfo(av:array of TVarEC; code:TCodeEC);
var
  no,i:integer;
  pa:PCustomShipInfo;
  ship:TShip;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ShipDeleteCustomShipInfo');
  ship:=TShip(av[1].VDW);
  if av[2].VType = vtStr then
  begin
    for i:=0 to ship.FCustomShipInfos.Count-1 do
    begin
      pa:=ship.FCustomShipInfos.Items[i];
      if pa.Delete then continue;
      if pa.InfoType<>av[2].VStr then continue;
      pa.Delete:=true;
      exit;
    end;
    exit;
  end;

  if (av[2].VDW>10000) and (av[2].VInt<>-1) then
  begin
    if (ship<>nil) and (ship.FCustomShipInfos.IndexOf(PCustomShipInfo(av[2].VDW))<0) then exit;
    PCustomShipInfo(av[2].VDW).Delete:=true;//ship can be 0 in this case
    exit;
  end;

  no:=av[2].VInt;

  if no<0 then exit;
  pa:=nil;
  for i:=0 to ship.FCustomShipInfos.Count-1 do
  begin
    pa:=ship.FCustomShipInfos.Items[i];
    if pa.Delete then continue;
    dec(no);
    if no<0 then break;
  end;
  if (no>=0) or (pa=nil) then exit;
  pa.Delete:=true;
end;

procedure SF_ShipFindCustomShipInfoByType(av:array of TVarEC; code:TCodeEC);
var
  i,no:integer;
  pa:PCustomShipInfo;
  ship:TShip;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ShipFindCustomShipInfoByType');
  ship:=TShip(av[1].VDW);
  no:=0;
  for i:=0 to ship.FCustomShipInfos.Count-1 do
  begin
    pa:=ship.FCustomShipInfos.Items[i];
    if pa.Delete then continue;
    if pa.InfoType=av[2].VStr then
    begin
      av[0].VInt:=no;
      exit;
    end;
    inc(no);
  end;
  av[0].VInt:=-1;
end;


procedure SF_ShipCustomShipInfoDescription(av:array of TVarEC; code:TCodeEC);
var
  i,no:integer;
  pa:PCustomShipInfo;
  ship:TShip;
  bl:TBlockParEC;
begin
  if (High(av) < 1) then raise Exception.Create('Error.Script ShipCustomShipInfoDescription');
  av[0].VStr:='';

  ship:=TShip(av[1].VDW);
  if av[2].VType = vtStr then
  begin
    pa:=nil;
    for i:=0 to ship.FCustomShipInfos.Count-1 do
    begin
      pa:=ship.FCustomShipInfos.Items[i];
      if pa.Delete then continue;
      if pa.InfoType=av[2].VStr then break;
    end;
    if (pa=nil) or (pa.InfoType<>av[2].VStr) then exit;
  end
  else if (av[2].VDW>10000) and (av[2].VInt<>-1) then
  begin
    pa:=PCustomShipInfo(av[2].VDW); //ship can be 0 in this case
    if (ship<>nil) and (ship.FCustomShipInfos.IndexOf(pa)<0) then exit;
  end else begin

    no:=av[2].VInt;
    if no<0 then exit;
    pa:=nil;
    for i:=0 to ship.FCustomShipInfos.Count-1 do
    begin
      pa:=ship.FCustomShipInfos.Items[i];
      if pa.Delete then continue;
      dec(no);
      if no<0 then break;
    end;
    if (no>=0) or (pa=nil) then exit;
  end;

  av[0].VStr:=pa.InfoDescription;
  if av[0].VStr='' then
  begin
    bl:=GR_BPLang.Block['ShipInfo'].Block['AddInfo'].Block['CustomInfos'].Block[pa.InfoType];
    if bl.Par_Count('Description')<>0 then av[0].VStr:=bl.Par['Description'];
  end;
  if (High(av) > 2) then pa.InfoDescription:=av[3].VStr;
end;

procedure SF_ShipCustomShipInfoData(av:array of TVarEC; code:TCodeEC);
var
  i,no,ind:integer;
  pa:PCustomShipInfo;
  ship:TShip;
begin
  if (High(av) < 3) then raise Exception.Create('Error.Script ShipCustomShipInfoData');
  av[0].VInt:=0;

  ship:=TShip(av[1].VDW);
  if av[2].VType = vtStr then
  begin
    pa:=nil;
    for i:=0 to ship.FCustomShipInfos.Count-1 do
    begin
      pa:=ship.FCustomShipInfos.Items[i];
      if pa.Delete then continue;
      if pa.InfoType=av[2].VStr then break;
    end;
    if (pa=nil) or (pa.InfoType<>av[2].VStr) then exit;
  end
  else if (av[2].VDW>10000) and (av[2].VInt<>-1) then
  begin
    pa:=PCustomShipInfo(av[2].VDW); //ship can be 0 in this case
    if (ship<>nil) and (ship.FCustomShipInfos.IndexOf(pa)<0) then exit;
  end else begin

    no:=av[2].VInt;
    if no<0 then exit;
    pa:=nil;
    for i:=0 to ship.FCustomShipInfos.Count-1 do
    begin
      pa:=ship.FCustomShipInfos.Items[i];
      if pa.Delete then continue;
      dec(no);
      if no<0 then break;
    end;
    if (no>=0) or (pa=nil) then exit;
  end;

  ind:=av[3].VInt;

  case ind of
    1: av[0].VInt:=pa.InfoData1;
    2: av[0].VInt:=pa.InfoData2;
    3: av[0].VInt:=pa.InfoData3;
    else raise Exception.Create('Error.Script ShipCustomShipInfoData ind');
  end;

  if (High(av) > 3) then
  case ind of
    1: pa.InfoData1:=av[4].VInt;
    2: pa.InfoData2:=av[4].VInt;
    3: pa.InfoData3:=av[4].VInt;
  end;
end;

procedure SF_ShipCustomShipInfoTextData(av:array of TVarEC; code:TCodeEC);
var
  i,no,ind:integer;
  pa:PCustomShipInfo;
  ship:TShip;
begin
  if (High(av) < 3) then raise Exception.Create('Error.Script ShipCustomShipInfoTextData');
  av[0].VStr:='';

  ship:=TShip(av[1].VDW);
  if av[2].VType = vtStr then
  begin
    pa:=nil;
    for i:=0 to ship.FCustomShipInfos.Count-1 do
    begin
      pa:=ship.FCustomShipInfos.Items[i];
      if pa.Delete then continue;
      if pa.InfoType=av[2].VStr then break;
    end;
    if (pa=nil) or (pa.InfoType<>av[2].VStr) then exit;
  end
  else if (av[2].VDW>10000) and (av[2].VInt<>-1) then
  begin
    pa:=PCustomShipInfo(av[2].VDW); //ship can be 0 in this case
    if (ship<>nil) and (ship.FCustomShipInfos.IndexOf(pa)<0) then exit;
  end else begin

    no:=av[2].VInt;
    if no<0 then exit;
    pa:=nil;
    for i:=0 to ship.FCustomShipInfos.Count-1 do
    begin
      pa:=ship.FCustomShipInfos.Items[i];
      if pa.Delete then continue;
      dec(no);
      if no<0 then break;
    end;
    if (no>=0) or (pa=nil) then exit;
  end;
  
  ind:=av[3].VInt;

  case ind of
    1: av[0].VStr:=pa.InfoTextData1;
    2: av[0].VStr:=pa.InfoTextData2;
    3: av[0].VStr:=pa.InfoTextData3;
    else raise Exception.Create('Error.Script ShipCustomShipInfoData ind');
  end;

  if (High(av) > 3) then
  case ind of
    1: pa.InfoTextData1:=av[4].VStr;
    2: pa.InfoTextData2:=av[4].VStr;
    3: pa.InfoTextData3:=av[4].VStr;
  end;

end;

procedure SF_StarCustomStarInfosCount(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script StarCustomStarInfosCount');
  av[0].VInt:=TStar(av[1].VDW).FCustomStarInfos.Count;
end;

procedure SF_StarAddCustomStarInfo(av:array of TVarEC; code:TCodeEC);
var
  cinfo:TCustomSystemInfo;
  star:TStar;
begin
  if(High(av) < 3) then raise Exception.Create('Error.Script StarAddCustomStarInfo');

  star:=TStar(av[1].VDW);
  cinfo:=TCustomSystemInfo.Create();
  star.FCustomStarInfos.Add(cinfo);

  cinfo.FType:=av[2].VStr;
  cinfo.FName:=av[3].VStr;
  if (High(av) > 3) then cinfo.FDist:=av[4].VInt else cinfo.FDist:=0;
  if (High(av) > 4) then cinfo.FIcon:=av[5].VStr else cinfo.FIcon:='';
  if (High(av) > 5) then cinfo.FInfo:=av[6].VStr else cinfo.FInfo:='';
  //examples
  // StarAddCustomStarInfo(GalaxyStar(2),'test','Test',0,'Bm.FormGalaxy2.Face2','Image:Bm.FormGalaxy2.Face4,Bm.FormGalaxy2.Face3');
  // StarAddCustomStarInfo(GalaxyStar(2),'test','Test2',1000,'','ShipName.Kling.1');
end;

procedure SF_StarDeleteCustomStarInfo(av:array of TVarEC; code:TCodeEC);
var
  no:integer;
  cinfo:TCustomSystemInfo;
  star:TStar;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script StarDeleteCustomStarInfo');
  star:=TStar(av[1].VDW);
  no:=av[2].VInt;
  if (no<0) or (no>=star.FCustomStarInfos.Count) then exit;
  cinfo:=star.FCustomStarInfos.Items[no];
  star.FCustomStarInfos.Delete(no);
  cinfo.Free;
end;

procedure SF_StarFindCustomStarInfoByType(av:array of TVarEC; code:TCodeEC);
var
  i:integer;
  cinfo:TCustomSystemInfo;
  star:TStar;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script StarFindCustomStarInfoByType');
  star:=TStar(av[1].VDW);
  for i:=0 to star.FCustomStarInfos.Count-1 do
  begin
    cinfo:=star.FCustomStarInfos.Items[i];
    if cinfo.FType<>av[2].VStr then continue;
    av[0].VInt:=i;
    exit;
  end;
  av[0].VInt:=-1;
end;

procedure SF_StarCustomStarInfoData(av:array of TVarEC; code:TCodeEC);
var
  no:integer;
  cinfo:TCustomSystemInfo;
  star:TStar;
begin
  if (High(av) < 3) then raise Exception.Create('Error.Script StarCustomStarInfoData');
  av[0].VStr:='';
  star:=TStar(av[1].VDW);
  no:=av[2].VInt;
  if (no<0) or (no>=star.FCustomStarInfos.Count) then exit;
  cinfo:=star.FCustomStarInfos.Items[no];

  if av[3].VStr = 'Name' then
  begin
    av[0].VStr:=cinfo.FName;
    if (High(av) > 3) then cinfo.FName:=av[4].VStr;
  end
  else if av[3].VStr = 'Dist' then
  begin
    av[0].VInt:=cinfo.FDist;
    if (High(av) > 3) then cinfo.FDist:=av[4].VInt;
  end
  else if av[3].VStr = 'Icon' then
  begin
    av[0].VStr:=cinfo.FIcon;
    if (High(av) > 3) then cinfo.FIcon:=av[4].VStr;
  end
  else if av[3].VStr = 'Info' then
  begin
    av[0].VStr:=cinfo.FInfo;
    if (High(av) > 3) then cinfo.FInfo:=av[4].VStr;
  end
  else raise Exception.Create('Error.Script StarCustomStarInfoData 2');

end;



procedure SF_ItemCanBeBroken(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  canBeBroken: boolean;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemCanBeBroken');
  canBeBroken:=false;
  obj:=TObject(av[1].VDW);
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if(item <> nil) then canBeBroken := (item.FItemType in CanBrokenEquipments) or (item.FItemType in CanBrokenArtefacts);
  av[0].VDW:=ord(canBeBroken);
end;

procedure SF_ItemFragility(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemFragility');
  obj:=TObject(av[1].VDW);
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  av[0].VFloat:=1;
  if(item <> nil) and (item is TEquipment) then av[0].VFloat:=TEquipment(item).Fragility;
end;

procedure SF_ItemDurability(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  durability,change: integer;
  item: TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemDurability');
  durability:=100;
  obj:=TObject(av[1].VDW);
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if(item <> nil) and (item is TEquipment) then
  begin
    durability:=Round((item as TEquipment).FDuration);
    if(High(av) > 1) then
    begin
      change := min(av[2].VInt,100);
      (item as TEquipment).FDuration:=change;
      (item as TEquipment).FBroken := change<=0;
    end;
  end;
  av[0].VInt:=durability;
end;

procedure SF_ItemLevel(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  level,level2: integer;
  item: TItem;
  ditem1,ditem2:TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemLevel');
  obj:=TObject(av[1].VDW);
  item:=nil;
  level:=0;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if(item <> nil) and (item.FItemType in ShipEquipments) then
  begin
    level:=(item as TEquipment).Level;
    if(High(av) > 1) then
    begin
      level2 := max(1,av[2].VInt);
      if item is TWeapon then
      begin
        ditem1:=CreateWeapon(TWeapon(item).WeaponInfo,item.FSize,level,item.FOwner);
        ditem2:=CreateWeapon(TWeapon(item).WeaponInfo,item.FSize,level2,item.FOwner);
      end else begin
        ditem1:=CreateEq(item.FItemType,item.FSize,level,item.FOwner);
        ditem2:=CreateEq(item.FItemType,item.FSize,level2,item.FOwner);
      end;
      case item.FItemType of
        t_Hull:
        begin
          THull(item).FAlloy:=TTechLevel(level2);
          THull(item).FHitProtect:=THull(item).FHitProtect+THull(ditem2).FHitProtect-THull(ditem1).FHitProtect;
        end;
        t_FuelTanks:
        begin
          TFuelTanks(item).FFuelTanksType:=TTechLevel(level2);
          TFuelTanks(item).FCapacity:=TFuelTanks(item).FCapacity+TFuelTanks(ditem2).FCapacity-TFuelTanks(ditem1).FCapacity;
          TFuelTanks(item).FFuel:=max(0,min(TFuelTanks(item).FFuel,TFuelTanks(item).FCapacity));
        end;
        t_Engine:
        begin
          TEngine(item).FEngineType:=TTechLevel(level2);
          TEngine(item).FSpeed:=TEngine(item).FSpeed+TEngine(ditem2).FSpeed-TEngine(ditem1).FSpeed;
          TEngine(item).FParsec:=TEngine(item).FParsec+TEngine(ditem2).FParsec-TEngine(ditem1).FParsec;
        end;
        t_Radar:
        begin
          TRadar(item).FRadarType:=TTechLevel(level2);
          TRadar(item).FRadius:=TRadar(item).FRadius+TRadar(ditem2).FRadius-TRadar(ditem1).FRadius;
        end;
        t_Scaner:
        begin
          TScaner(item).FScanerType:=TTechLevel(level2);
          TScaner(item).FScanProtect:=TScaner(item).FScanProtect+TScaner(ditem2).FScanProtect-TScaner(ditem1).FScanProtect;
        end;
        t_RepairRobot:
        begin
          TRepairRobot(item).FRepairRobotType:=TTechLevel(level2);
          TRepairRobot(item).FRecoverHitPoints:=TRepairRobot(item).FRecoverHitPoints+TRepairRobot(ditem2).FRecoverHitPoints-TRepairRobot(ditem1).FRecoverHitPoints;
        end;
        t_CargoHook:
        begin
          TCargoHook(item).FCargoHookType:=TTechLevel(level2);
          TCargoHook(item).FPickUpSize:=TCargoHook(item).FPickUpSize+TCargoHook(ditem2).FPickUpSize-TCargoHook(ditem1).FPickUpSize;
          TCargoHook(item).FHookRadius:=TCargoHook(item).FHookRadius+TCargoHook(ditem2).FHookRadius-TCargoHook(ditem1).FHookRadius;
          TCargoHook(item).FSpeedMin:=TCargoHook(item).FSpeedMin+TCargoHook(ditem2).FSpeedMin-TCargoHook(ditem1).FSpeedMin;
          TCargoHook(item).FSpeedMax:=TCargoHook(item).FSpeedMax+TCargoHook(ditem2).FSpeedMax-TCargoHook(ditem1).FSpeedMax;
        end;
        t_DefGenerator:
        begin
          TDefGenerator(item).FTechLevel:=TTechLevel(level2);
          TDefGenerator(item).FDefFactor:=TDefGenerator(item).FDefFactor+TDefGenerator(ditem2).FDefFactor-TDefGenerator(ditem1).FDefFactor;
        end;

        else if item.FItemType in Weapons then
        begin
          TWeapon(item).FTechLevel:=TTechLevel(level2);
          TWeapon(item).FRadius:=TWeapon(item).FRadius+TWeapon(ditem2).FRadius-TWeapon(ditem1).FRadius;
          TWeapon(item).FMinDamage:=TWeapon(item).FMinDamage+TWeapon(ditem2).FMinDamage-TWeapon(ditem1).FMinDamage;
          TWeapon(item).FMaxDamage:=TWeapon(item).FMaxDamage+TWeapon(ditem2).FMaxDamage-TWeapon(ditem1).FMaxDamage;
          TWeapon(item).FMaxAmmunition:=TWeapon(item).FMaxAmmunition+TWeapon(ditem2).FMaxAmmunition-TWeapon(ditem1).FMaxAmmunition;
          TWeapon(item).FAmmunition:=max(0,TWeapon(item).FAmmunition+TWeapon(ditem2).FAmmunition-TWeapon(ditem1).FAmmunition);
        end;
      end;


      ditem1.Free;
      ditem2.Free;
    end;
  end;
  av[0].VInt:=level;
end;

procedure SF_ContainerFuel(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ContainerFuel');
  obj:=TObject(av[1].VDW);

  if obj is TFuelTanks then
  begin
    av[0].VInt:=TFuelTanks(obj).FFuel;
    if High(av) > 1 then TFuelTanks(obj).FFuel:=av[2].VInt;
  end
  else if obj is TCistern then
  begin
    av[0].VInt:=TCistern(obj).FFuel;
    if High(av) > 1 then TCistern(obj).FFuel:=av[2].VInt;
  end
  else av[0].VInt:=0;

end;


procedure SF_ItemCharge(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemCharge');
  obj:=TObject(av[1].VDW);

  if obj is TArtefactTransmitter then
  begin
    av[0].VInt:=TArtefactTransmitter(obj).FPower;
    if High(av) > 1 then TArtefactTransmitter(obj).FPower:=av[2].VInt;
  end
  else av[0].VInt:=0;

end;

procedure SF_MissilesToRearm(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  ammo,ammo2: integer;
  item: TItem;
  ditem1,ditem2:TItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script MissilesToRearm');
  obj:=TObject(av[1].VDW);
  ammo:=0;
  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if(item <> nil) and (TWeapon(item).WeaponInfo.ShotType in SetMissileWeapon) then
  begin
    ammo:=TWeapon(item as TEquipment).FMaxAmmunition-TWeapon(item as TEquipment).FAmmunition;
    if(High(av) > 1) then
    begin
      ammo2 := av[2].VInt;
      TWeapon(item as TEquipment).FAmmunition:=max(0,min(TWeapon(item as TEquipment).FMaxAmmunition,ammo2+TWeapon(item as TEquipment).FAmmunition));
    end;
  end;
  av[0].VInt:=ammo;
end;

procedure SF_WeaponAmmunition(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
  weapon:TWeapon;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script WeaponAmmunition');
  obj:=TObject(av[1].VDW);

  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if (item=nil) or not (item is TWeapon) then
  begin
    av[0].VInt:=0;
    exit;
  end;

  weapon:=item as TWeapon;

  av[0].VInt:=weapon.FAmmunition;
  if High(av) > 1 then weapon.FAmmunition:=av[2].VInt;

end;

procedure SF_WeaponMaxAmmunition(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
  weapon:TWeapon;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script WeaponAmmunition');
  obj:=TObject(av[1].VDW);

  item:=nil;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if (item=nil) or not (item is TWeapon) then
  begin
    av[0].VInt:=0;
    exit;
  end;

  weapon:=item as TWeapon;

  av[0].VInt:=weapon.FMaxAmmunition;
  if High(av) > 1 then weapon.FMaxAmmunition:=av[2].VInt;

end;



procedure SF_ShipSpecialBonuses(av:array of TVarEC; code:TCodeEC);
var
  ship:TShip;
  bon:TBonusItem;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SF_ShipSpecialBonuses');
  ship:=TShip(av[1].VDW);
  bon:=TBonusItem(av[2].VInt);
  if (High(av) > 2) and (av[3].VType=vtStr) and (av[3].VStr='Total') then av[0].VInt:=ship.CalcSpecialBonus(bon)
  else
  begin
    av[0].VInt:=ship.GetSpecialScriptBonus(bon);
    if (High(av) > 2) then ship.SetSpecialScriptBonus(bon,av[3].VInt);
  end;
end;

procedure SF_ItemExtraSpecials(av:array of TVarEC; code:TCodeEC);
var
  item:TEquipment;
  no,cnt:integer;
begin
  if (High(av) < 1) then raise Exception.Create('Error.Script SF_ItemExtraSpecials');

  if (High(av) = 1) and (TItem(av[1].VDW).FItemType in Goods) then begin av[0].VInt:=0; exit; end;
  
  item:=TEquipment(av[1].VDW);

  if item.FExtraSpecials=nil then cnt:=0
  else cnt:=item.FExtraSpecials.Count;

  if High(av) < 2 then
  begin
    av[0].VInt:=cnt;
    exit;
  end;

  no:=av[2].VInt;
  if (no<0) or (no>=cnt) then
  begin
    av[0].VInt:=-1;
    exit;
  end;

  av[0].VInt:=PExtraSpecial(item.FExtraSpecials.Items[no]).no-1;

end;

procedure SF_ItemExtraSpecialsCountByType(av:array of TVarEC; code:TCodeEC);
var
  item:TEquipment;
  bon,i:integer;
  pexsp:PExtraSpecial;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SF_ItemExtraSpecialsCountByType');

  if TItem(av[1].VDW).FItemType in Goods then begin av[0].VInt:=0; exit; end;
  item:=TEquipment(av[1].VDW);

  bon:=av[2].VInt+1;
  av[0].VInt:=0;
  if item.FExtraSpecials = nil then exit;
  
  for i:=0 to item.FExtraSpecials.Count-1 do
  begin
    pexsp:=item.FExtraSpecials.Items[i];
    if pexsp.no = bon then begin av[0].VInt:=pexsp.cnt; exit; end;
  end;


end;


procedure SF_ItemExtraSpecialsAddByType(av:array of TVarEC; code:TCodeEC);
var
  item:TEquipment;
  bon,i,j,cnt:integer;
  pexsp:PExtraSpecial;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SF_ItemExtraSpecialsAddByType');
  item:=TEquipment(av[1].VDW);
  bon:=av[2].VInt+1;
  if(High(av) > 2) then cnt:=av[3].VInt else cnt:=1;

  if (item.FExtraSpecials = nil) and (cnt>0) then item.FExtraSpecials:=TList.Create;

  pexsp:=nil;j:=-1;
  for i:=0 to item.FExtraSpecials.Count-1 do
    if PExtraSpecial(item.FExtraSpecials.Items[i]).no = bon then begin pexsp:=item.FExtraSpecials.Items[i]; j:=i; break; end;

  if pexsp<>nil then
  begin
    pexsp.cnt:=pexsp.cnt+cnt;
    if pexsp.cnt<=0 then
    begin
      dispose(pexsp);
      item.FExtraSpecials.Delete(j);
      if item.FExtraSpecials.Count = 0 then
      begin
        item.FExtraSpecials.Free;
        item.FExtraSpecials:=nil;
      end;
    end;
  end else begin
    new(pexsp);
    item.FExtraSpecials.Add(pexsp);
    pexsp.no:=bon;
    pexsp.cnt:=cnt;
  end;

end;

procedure SF_ItemExtraSpecialsDeleteByType(av:array of TVarEC; code:TCodeEC);
var
  item:TEquipment;
  bon,i,j,cnt:integer;
  pexsp:PExtraSpecial;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SF_ItemExtraSpecialsDeleteByType');
  item:=TEquipment(av[1].VDW);
  bon:=av[2].VInt+1;
  if(High(av) > 2) then cnt:=av[3].VInt else cnt:=1;

  if item.FExtraSpecials = nil then exit;

  pexsp:=nil;j:=-1;
  for i:=0 to item.FExtraSpecials.Count-1 do
    if PExtraSpecial(item.FExtraSpecials.Items[i]).no = bon then begin pexsp:=item.FExtraSpecials.Items[i]; j:=i; break; end;

  if pexsp<>nil then
  begin
    pexsp.cnt:=pexsp.cnt-cnt;
    if pexsp.cnt<=0 then
    begin
      dispose(pexsp);
      item.FExtraSpecials.Delete(j);
      if item.FExtraSpecials.Count = 0 then
      begin
        item.FExtraSpecials.Free;
        item.FExtraSpecials:=nil;
      end;
    end;
  end;
end;

procedure SF_ExecuteCodeFromString(av:array of TVarEC; code:TCodeEC);
var tstr:WideString;
  tempCode:TCodeEC;
  tmpScr:TScript;
  i,cnt:integer;
  v:TVarEC;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script SF_ExecuteCodeFromString');

  tstr:=av[1].VStr;

  if High(av) = 1 then
  begin
    if code<>nil then InterpretAndExecuteString(tstr,code.LocalVar)
    else InterpretAndExecuteString(tstr);
    exit;
  end;

  tmpScr:=GScriptCur;


  tempCode:=CompileCodeFromString(tstr);

  tempCode.LinkAll(GScriptGlobalVarGame);
  tempCode.LinkAll(GScriptFun);
  tempCode.FScriptFunLinked:=true;
  if code<>nil then tempCode.LinkAll(code.LocalVar);

  cnt:=(High(av)-1) div 2;

  for i:=1 to cnt do
    tempCode.LocalVar.Add( av[2*i].VStr, av[2*i+1].VType).Assume( av[2*i+1], true );


  try
    tempCode.Run(GScriptCP);
  except
    on E: EBreakMessageGI do;
    on E: Exception do
    begin
      SFT(E.ClassName + ' '+E.Message);
      PrintFunctionCallHistory;
      SFT('Error while executing code from string: ');
      if Length(tstr)<=256 then SFT(tstr)
      else SFT(Copy(tstr,1,256)+' ...');

      raise;
    end;
  end;

  if High(av) mod 2 = 0 then
  begin
    av[0].Assume( tempCode.LocalVar.GetVar(av[High(av)].VStr), true );
  end;

  GScriptCur:=tmpScr;

  tempCode.Free;

end;


procedure SF_GenerateCodeStringFromBlock(av:array of TVarEC; code:TCodeEC);
var path:WideString;
    i,cnt:integer;
    bpp: TBlockParEC;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script SF_GenerateCodeStringFromBlock');
  av[0].VStr:='';
  path:=av[1].VStr;
  cnt:=GetCountParEC(path,'.');
  bpp:=GR_BPLang;
  for i:=0 to cnt-1 do
  begin
    if bpp.Block_Count(GetStrParEC(path,i,'.')) = 0 then
    begin
      SFT('Warning.Script SF_GenerateCodeStringFromBlock - cant find block '+av[1].VStr);
      exit;
    end;
    bpp:=bpp.Block[GetStrParEC(path,i,'.')];
  end;
  av[0].VStr:=bpp.GenerateCodeString();
  if av[0].VStr='' then SFT('Warning.Script SF_GenerateCodeStringFromBlock - no code at '+av[1].VStr);
end;

procedure SF_ItemOnUseCode(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  sitem: TScriptItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemOnUseCode');
  obj:=TObject(av[1].VDW);
  sitem:=nil;
  if(obj is TItem) then sitem:=TScriptItem(TItem(obj).FScriptItem);
  if(obj is TScriptItem) then sitem:=TScriptItem(obj);
  if(sitem <> nil) then
  begin
    av[0].VStr:=sitem.FOnUseCode;
    if(High(av) > 1) then sitem.FOnUseCode:=av[2].VStr;
  end else av[0].VStr:='';
end;

//OnUse code can use ScriptItemActShip and ScriptItemActParam (setting 1 will close form)

procedure SF_ItemOnActCode(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  sitem: TScriptItem;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script ItemOnActCode');
  obj:=TObject(av[1].VDW);
  sitem:=nil;
  if(obj is TItem) then sitem:=TScriptItem(TItem(obj).FScriptItem);
  if(obj is TScriptItem) then sitem:=TScriptItem(obj);
  if(sitem <> nil) then
  begin
    av[0].VStr:=sitem.FOnActCode;
    if(High(av) > 3) then
    begin
      if sitem.FOnActCompiledCode<>nil then sitem.FOnActCompiledCode.Free;
      sitem.FOnActCompiledCode:=nil;
      sitem.FOnActCode:='['+av[3].VStr+'|'+av[4].VStr+']'+av[2].VStr;
    end;
    if(High(av) > 1) then
    begin
      if sitem.FOnActCompiledCode<>nil then sitem.FOnActCompiledCode.Free;
      sitem.FOnActCompiledCode:=nil;

      if High(av) > 3 then sitem.FOnActCode:='['+av[3].VStr+'|'+av[4].VStr+']'+av[2].VStr
      else if High(av) = 3 then sitem.FOnActCode:='['+av[3].VStr+']'+av[2].VStr
      else sitem.FOnActCode:=av[2].VStr;
    end;
  end else av[0].VStr:='';
end;
//item owner = CurShip, ScriptItemActShip

//if actcode is from Lang (info,art,useless) then filters can be used
//OnActCodeTypes limits what events will be processed
//OnActStepTypes limits what OnStep events will be processed

//    on actions
//t_OnWeaponShot on non-missile weapon shot, Object1 is target, Object2 is weapon
//Param = damage sent (before protection)
//or hit/miss flag when hitting missile
//or extra explosion damage when hitting item (default = 0)

//t_OnWeaponShot2
//same but Param is damage set

{                   dtEnergy, dtSplinter, dtMissile,
                    dtDecelerateW, dtDestruct, dtDrain,
                    dtShock, dtAcid, dtMagnetic,
                    dtDecelerateA, dtDecelerateAEx, //art effect
                    dtUndefendable, dtNonLethal,    //reflect, shock
                    dtTargetingScan,dtTargetingDamaged, //targeting
                    dtTargetingMoreDrop,dtTargetingDropCargo,
                    dtTargetingReduceEngine,dtTargetingBlockWeapon,dtTargetingBlockDroid)}

//t_OnMissileShot on create missile, Object1 is missile, Object2 is weapon

//t_OnMissileShot2 hitting ship with missile,
//Object1 is target, Object2 is missile
//Param is damage set

//t_OnGettingWeaponHit,t_OnGettingMissileHit - we take weapon/missile hit, Object1 is attacker/missile owner(if any) Object2 is weapon/missile
//Param is damage set

//t_OnDealingDamage - before applying damage to target hull, Object1 = target ship, Param = damage
//t_OnDealingFatalDamage - on killing ship (before actual damage is applied and all item drops and statistic change), Object1 = target ship

//t_OnTakingDamageEn,t_OnTakingDamageSp,t_OnTakingDamageMi - before applying weapon damage (energy,splinter or missile) to hull
//t_OnTakingDamage - before applying untyped damage (star, asteroid, explosion) to hull
//Object1 = damage source (ship/missile/asteroid/star/item/none), Param = damage

//t_OnDroidRepair - on repair, Param = hp to heal
//t_OnScan - on scan, Object1 = ship

//t_OnItemPickUp - after item pickup, Object = item
//Param - result of action:
//0 - item will be picked normally
//anything else - item will be deleted


//t_OnStep    on steps
//called only when item is in ship (CurShip) or in open space
//Object1 = system containing item, if item is in space
//Param = step num (1-10)

//t_OnAnotherItem   when clicking with this item on some equipment (processed first)
//t_OnAnotherItem2  when clicking with some equipment on this item
//Object1 = second item, ship = CurShip (Player, tranc, ruin)
//Param - result of action:
//0 - item stays in hand / is put in hold (default is 0 unless both events work)
//1 - item will be expended (for one-use items)
//2 - item stays in hand even if clicked on hold item
//3 - item expended and form closed
//anything else - same as 0

//t_OnAnotherGoods  when clicking with goods on this item
//Object1 = goods type, Object2 = goods cnt, ship = CurShip (Player, tranc, ruin)
//Param - result of action:
//0 - goods stay in hand / is put in hold (default is 0)
//N>0 - N cnt will be expended
//N<0 - |N| cnt will be expended and form closed


//t_OnItemHit (called for item)
//when ship/missile hits item
//CurShip - ship/missile owner/0
//Object1 = weapon(item)/missile
//Object2 = system containing item
//Param - explosion damage

//t_OnMissileHittingObject (called for ship)
//when missile hits item/asteroid
//CurShip - missile owner
//Object1 = object
//Object2 = missile
//Param - 0 miss, 1 hit (default is 1)

//t_OnEnteringForm,t_OnLeavingForm, t_OnReEnteringForm (ReEnter only for Ship form mostly when player moves some items around)
//for ship and scaner form CurShip = current ship, all others ship = Player

//t_OnPlayerSkillIncrease
//when player ups skill on ship form
//CurShip - player,station or tranc

//t_OnPlayerTalkedWithShip
//when player finishes dialog with some ship
//Object1 = ship

//t_OnShipTalkedWithPlayer
//when some ship finishes dialog with player
//Object1 = ship

//t_OnDropItem,t_OnDropItemFixed
//CurShip - ship that drops item
//Object1 = item
//difference:
//t_OnDropItem - item will move some distance before stopping (can be stopped with StopMovingItem)
//item is not in ship nor in system when event activates
//non-zero Param will prevent item from being dropped in system (but will not return it to ship by itself)

//t_OnDropItemFixed - item dropped to fixed position (player drops like that) if dropped within star damage radius, item will explode immediately, unless script changes its coords
//item is not in ship and already in system (and not yet destroyed if dropped on sun)
//does not use Param because at this point script can just remove item from system manually if it wants to

//t_OnReduceEqBattle,t_OnReduceEqUse,t_OnReduceEqForce,t_OnReduceEqForsage
//when item durability is reduced (by enemy fire/from using it/by bertors aura/from using forsage)
//CurShip - ship
//Object1 = item that is wearing down
//Param - value of wearing (multiplied by 1000, so full durability bar = 100000)

//t_OnItemDestroy - before item is destroyed in any way, only called for that item

//t_OnPlayerChangeHull
//Object1 - new hull (called just before switch)
//Object2 - current hull
//if new hull has actcode it also receives same event but after switch with
//Object1 - now current hull
//Object2 - old hull (could be 0 if it was sold)

//t_OnPlayerUseMM
//CurShip - player/trank/ruin
//Object1 - eq
//Object2 - MM

//t_OnItemEquip,t_OnItemDeEquip - when item is equiped/removed in any way, only called for that item


//t_OnTrancPacking
//CurShip - trank or his owner
//Object1 - artefact
//Object2 - location (ship or planet/ruin storage)

//t_OnShipBuysGoods,t_OnShipSellsGoods - ship buys/sells goods
//CurShip - ship
//Param - total cost
//Object1 - goods type (t_Food, etc)
//Object2 - goods count

//t_OnShowingItemInfo - before showing item info window
//CurShip - Player/trank/station/scanned ship/0
//Object1 - cur star (for starmap), cur planet (for eq shop, uninhabited planet), cur station (eq shop), 0

//t_OnShowingItemInfo - before showing ship info window
//CurShip - ship

//t_OnNonStandartEqChange - when ship eq changed by script
//automatically fired on change by ItemIsInUse and pressing hot eq set buttons
//should be fired manually in other cases
//CurShip - ship

//t_OnStartAB - when AB starts
//CurShip - player
//Object1 - ABship for player

//t_OnABItemDrop - when players gets item after killing enemy in arcade battle (fired before item is added to player inventory)
//CurShip - player
//Object1 - item

//t_OnCheckingUsability - item is picked up
//CurShip - player or ruin/tranc on ship form
//Object1 - eq, if code returns 1 this item will be highlighted (like when picking micromodule)

//t_OnCheckingUsability2 - another item is picked up, fires for equipped items, if code returns 1 they will be highlighted
//CurShip - player or ruin/tranc on ship form
//Object1 - item in hand

//t_OnCheckingUsabilityGoods - goods are picked up, fires for equipped items, if code returns non-zero N, then abs(N) conut of goods will be spent, and, if N is negative, form will close
//CurShip - player or ruin/tranc on ship form
//Object1 = goods type
//Object2 = goods cnt

//t_OnDeath - as name says
//CurShip - dying ship

procedure SF_CreateActCodeEvent(av:array of TVarEC; code:TCodeEC);
var
  actType:TActionType;
  obj,obj1,obj2:TObject;
  ship:TShip;
  param:integer;
begin
  if High(av) < 2 then raise Exception.Create('Error.Script ItemOnActCode');
  actType:=TActionType(av[1].VInt); //event type
  obj:=TObject(av[2].VDW);          //ship or item
  av[0].VInt:=0;

  if obj is TShip then
  begin
    if High(av) >= 3 then obj1:=TObject(av[3].VDW) else obj1:=nil;
    if High(av) >= 4 then obj2:=TObject(av[4].VDW) else obj2:=nil;
    if High(av) >= 5 then param:=av[5].VInt else param:=0;
    av[0].VInt:=(obj as TShip).ScriptItemsAct(actType,obj1,obj2,param);
  end
  else if obj is TItem then
  begin
    if High(av) >= 3 then ship:=TShip(av[3].VDW) else ship:=nil;//different order of arguments!
    if High(av) >= 4 then obj1:=TObject(av[4].VDW) else obj1:=nil;
    if High(av) >= 5 then obj2:=TObject(av[5].VDW) else obj2:=nil;
    if High(av) >= 6 then param:=av[6].VInt else param:=0;
    if TItem(obj).FScriptItem<>nil then av[0].VInt:=TScriptItem(TItem(obj).FScriptItem).ExecuteActCode(actType,ship,obj1,obj2,param);
    if obj is TEquipmentWithActCode then av[0].VInt:=ExecuteActCode(TItem(obj),actType,ship,obj1,obj2,param);
  end;
end;

procedure SF_CurItem(av:array of TVarEC; code:TCodeEC);
begin
  if GScriptActCodeItem.Count<1 then av[0].VDW:=cardinal(GItem_Used)
  else av[0].VDW:=cardinal(GScriptActCodeItem.Items[GScriptActCodeItem.Count-1]);
end;

procedure SF_CurInfo(av:array of TVarEC; code:TCodeEC);
begin
  if GScriptActCodeInfo.Count<1 then av[0].VDW:=0
  else av[0].VDW:=cardinal(GScriptActCodeInfo.Items[GScriptActCodeInfo.Count-1]);
end;

procedure SF_ScriptItemActShip(av:array of TVarEC; code:TCodeEC);
begin
  if GScriptActCodeShip.Count<1 then av[0].VDW:=0
  else av[0].VDW:=cardinal(GScriptActCodeShip.Items[GScriptActCodeShip.Count-1]);
end;

procedure SF_ScriptItemActObject1(av:array of TVarEC; code:TCodeEC);
begin
  if GScriptActCodeObject1.Count<1 then av[0].VDW:=0
  else av[0].VDW:=cardinal(GScriptActCodeObject1.Items[GScriptActCodeObject1.Count-1]);
end;

procedure SF_ScriptItemActObject2(av:array of TVarEC; code:TCodeEC);
begin
  if GScriptActCodeObject2.Count<1 then av[0].VDW:=0
  else av[0].VDW:=cardinal(GScriptActCodeObject2.Items[GScriptActCodeObject2.Count-1]);
end;

procedure SF_ScriptItemActionType(av:array of TVarEC; code:TCodeEC);
var res:boolean;
begin
  if GScriptActCodeType.Count<1 then av[0].VDW:=0
  else if High(av)<=0 then av[0].VDW:=cardinal(GScriptActCodeType.Items[GScriptActCodeType.Count-1])
  else begin
    res:=(integer(GScriptActCodeType.Items[GScriptActCodeType.Count-1]) = av[1].VInt);
    if res and (High(av)>1) then res:=(integer(GScriptActCodeParam.Items[GScriptActCodeParam.Count-1]) = av[2].VInt);
    av[0].VDW:=ord(res);
  end;
end;

procedure SF_ScriptItemActParam(av:array of TVarEC; code:TCodeEC);
begin
  if GScriptActCodeParam.Count<1 then av[0].VInt:=0
  else begin
    av[0].VInt:=integer(GScriptActCodeParam.Items[GScriptActCodeParam.Count-1]);
    if(High(av) > 0) then GScriptActCodeParam.Items[GScriptActCodeParam.Count-1]:=pointer(av[1].VInt);
  end;
end;

procedure SF_OnUseCodeTranclucator(av:array of TVarEC; code:TCodeEC);
var
  art:TArtefactTranclucator;
  tran:TTranclucator;
  i:integer;
  angle:single;
  su: PStorageUnit;
  star:TStar;
  ship:TShip;
begin
  if (GItem_Used <> nil) and (GItem_Used is TArtefactTranclucator) then art:=TArtefactTranclucator(GItem_Used)
  else if (High(av) >= 1) and (av[1].VDW<>0) and (TObject(av[1].VDW) is TArtefactTranclucator) then art:=TArtefactTranclucator(av[1].VDW)
  else exit;

  if Player = nil then Exit;
  tran := art.FShip as TTranclucator;
  av[0].VDW:=Cardinal(tran);
  if Player.InNormalSpace then
    begin
      GR_SC.Play('Sound.UseATranc');

      art.FShip := nil;
      tran.FCurStar := Player.FCurStar;
      Player.FCurStar.FShips.Add(tran);
      angle := Rnd(0, 360, Player.FCurStar.FRnd * Galaxy.FTurn * integer(tran.FId)) * pi / 180;
      tran.FPos.x := Player.FPos.x + sin(angle) * 100;
      tran.FPos.y := Player.FPos.y - cos(angle) * 100;
      tran.FGraphShip.Pos := tran.FPos;
      tran.FProprietor := Player;

      i:=Player.FArtefacts.IndexOf(art);
      if i>=0 then Player.FArtefacts.Delete(i);
      i:=Player.FEquipments.IndexOf(art);
      if i>=0 then Player.FEquipments.Delete(i);

      art.Free;
      if GItem_Used=art then GItem_Used:=nil;
      Player.CalcParam;

      tran.NextDay;
      Player.FAchievementStats.CheckConditionAchTranclucators();

      star:=Player.FCurStar;
      if Player.IsChameleon then for i:=0 to star.FShips.Count-1 do
      begin
        ship:=star.FShips[i];
        if not (ship is TKling) then continue;
        if ship.IsCustomFaction then continue;
        TKling(ship).DetectChameleon(Player);
      end;
    end
    else
    begin
      if GFormShip.PlaceShipToHangar(tran) then
      begin
        art.FShip := nil;
        i:=Player.FArtefacts.IndexOf(art);
        if i>=0 then Player.FArtefacts.Delete(i);
        i:=Player.FEquipments.IndexOf(art);
        if i>=0 then Player.FEquipments.Delete(i);
        
        for i:=0 to Player.FStorage.Count-1 do
        begin
          su:=Player.FStorage.Items[i];
          if su.FItem<>art then continue;
          Player.FStorage.Delete(i);
          Player.StorageToMsgPlayer();
          Dispose(su);
          break;
        end;

        art.Free;
        if GItem_Used=art then GItem_Used:=nil;
        Player.CalcParam;
        //GFormShip.Update;
        GR_SC.Play('Sound.UseATranc');
        MessageBoxGI(GFormShip, CTExt('FormShip.UseTranclucator'), GIMB_OK or GIMB_IconInfo);
      end
      else
      begin
        GR_SC.Play('Sound.NoMoney');
        MessageBoxGI(GFormShip, CTExt('FormShip.NotUseTranclucator'), GIMB_Cancel or GIMB_IconInfo);
      end;
    end;
end;

procedure SF_OnUseCodeTransmitter(av:array of TVarEC; code:TCodeEC);
var
  art:TArtefactTransmitter;
  showMessage:boolean;
  //day:integer;
begin
  if (GItem_Used <> nil) and (GItem_Used is TArtefactTransmitter) then art:=TArtefactTransmitter(GItem_Used)
  else if (High(av) >= 1) and (av[1].VDW<>0) and (TObject(av[1].VDW) is TArtefactTransmitter) then art:=TArtefactTransmitter(av[1].VDW)
  else exit;

  if High(av) > 1 then showMessage:=(av[2].VInt<>0) else showMessage:=true;

  if not Player.InNormalSpace then
  begin
    if showMessage then
    begin
      GR_SC.Play('Sound.NoMoney');
      MessageBoxGI(GFormShip, CTExt('FormShip.UseOnlyInSpace'), GIMB_Cancel or GIMB_IconInfo);
      exit;
    end;
  end;

  if Player.UseTransmitter(art) then
  begin
      {day := mEIllness[EIllRadiation].Time;
      if (Player.FmEInfections[EIllRadiation].Infection = 0) then
      begin
        Player.FmEInfections[EIllRadiation].Infection := 0.9;
        Player.FmEInfections[EIllRadiation].InfectionDay := Galaxy.FTurn;
        inc(Player.FmEInfections[EIllRadiation].InfectionCount);
        Player.FAchievementStats.CheckConditionAchIll();
        Player.FmEInfections[EIllRadiation].InfectionEndDay := Galaxy.FTurn + day + RndOut(0, Round(day / 2), Player.FRndOut);
        MsgPlayerAdd(mp_Galaxy, Galaxy.FTurn, SRF2(CTExt('Illness.ExtraIllness.' + inttostr(EIllRadiation) + '.Start'), txtStandart, '<Date>', Galaxy.GameDateTxt, '<Name>', mEIllness[EIllRadiation].Name), 'TMUseFisrt');
      end
      else
      begin
        Player.FmEInfections[EIllRadiation].Infection := max(0.5,Player.FmEInfections[EIllRadiation].Infection - 0.05);
        Player.FmEInfections[EIllRadiation].InfectionEndDay := Player.FmEInfections[EIllRadiation].InfectionEndDay + Round(day / 2) + RndOut(0, Round(day / 3), Player.FRndOut);
        MsgPlayerAdd(mp_Galaxy, Galaxy.FTurn, SRF2(CTExt('Illness.ExtraIllness.' + inttostr(EIllRadiation) + '.Next'), txtStandart, '<Date>', Galaxy.GameDateTxt, '<Name>', mEIllness[EIllRadiation].Name), 'TMUseNext');
      end;
      GFormShip.FPanelMain.MsgShow;
      }
      if showMessage then
      begin
        GR_SC.Play('Sound.UseATranc');
        MessageBoxGI(GFormShip, SRF1(CTExt('FormShip.UseTransmitter'), clr, '<Star>', Player.FCurStar.FName), GIMB_Cancel or GIMB_IconInfo);
      end;
    end
    else
    begin
      if showMessage then
      begin
        GR_SC.Play('Sound.NoMoney');
        MessageBoxGI(GFormShip, SRF1(CTExt('FormShip.NotUseTransmitter'), clr, '<Count>', inttostr(MinTransmitterPower - (GItem_Used as TArtefactTransmitter).FPower)), GIMB_Cancel or GIMB_IconInfo);
      end;
  end;
end;

procedure SF_OnUseCodeBlackHole(av:array of TVarEC; code:TCodeEC);
var
  art:TArtefact;
  i: integer;
  a, r: single;
  //tran: TTranclucator;
  angle: single;
  hole: THole;
  s: WideString;
  gevent:TGalaxyEvent;
  tstr:WideString;
begin
  av[0].VDW:=0;

  if (GItem_Used <> nil) and (GItem_Used is TArtefact) then art:=TArtefact(GItem_Used)
  else if (High(av) >= 1) and (av[1].VDW<>0) and (TObject(av[1].VDW) is TArtefact) then art:=TArtefact(av[1].VDW)
  else exit;

  //if art.FItemType <> t_ArtBlackHole then exit;
  if Player = nil then Exit;

  if not Player.InNormalSpace then
  begin
    GR_SC.Play('Sound.NoMoney');
    MessageBoxGI(GFormShip, CTExt('FormShip.UseOnlyInSpace'), GIMB_Cancel or GIMB_IconInfo);
    exit;
  end;

    i:=Player.FArtefacts.IndexOf(art);
    if i>=0 then Player.FArtefacts.Delete(i);
    i:=Player.FEquipments.IndexOf(art);
    if i>=0 then Player.FEquipments.Delete(i);
    art.Free;
    if GItem_Used=art then GItem_Used:=nil;
    Player.CalcParam;

    hole := THole.Create;
    av[0].VDW:=Cardinal(hole);
    hole.Init;
    hole.FGraphHole.State := 1;
    hole.FStar1 := Player.FCurStar;

    a := ArcTan2(Player.FPos.x, -Player.FPos.y);
    r := max(Player.FCurStar.FSafeRadius + 100, sqrt(Dist2(Player.FPos, Dxy(0, 0))) + 200);

    hole.FPos1 := Dxy(sin(a) * r, -cos(a) * r);

    hole.FStar2 := nil;
    for i := 0 to Galaxy.FStars.Count - 1 do
    begin
      if not TStar(Galaxy.FStars.Items[i]).Visible then continue;
      r := Dist2(Player.FCurStar.FPos, TStar(Galaxy.FStars.Items[i]).FPos);
      if (r > (20 * 20)) and (r < (50 * 50)) then
      begin
        if (hole.FStar2 = nil) or (RndOut(0, 100, Player.FRndOut) < 50) then
        begin
          hole.FStar2 := Galaxy.FStars.Items[i];
          if RndOut(0, 100, Player.FRndOut) < 20 then break;
        end;
      end;
    end;
    if hole.FStar2 = nil then hole.FStar2 := Player.FCurStar;

    a := Angle360ToRad(Rnd(0, 359, Galaxy.FRndOut));
    r := Rnd(1000, 2000, Galaxy.FRndOut);
    hole.FPos2 := Dxy(sin(a) * r, -cos(a) * r);

    hole.FTurnCreate := Galaxy.FTurn;
    hole.FType := 1;
    GFormStarMap.FOpenHole := hole;
    Galaxy.FHoles.Add(hole);

    gevent := NewEvent('PlayerUsesSubportal');
    gevent.Add(hole.FId);
    gevent.Add(hole.FTurnCreate);

    Galaxy.CUpdateIn(523);
    GFormShip.ButtonExit(nil);

end;


procedure SF_OnUseCodeMissileDef(av:array of TVarEC; code:TCodeEC);
var
  //art:TArtefact;
  i:integer;
begin
  //if (GItem_Used <> nil) and (GItem_Used is TArtefact) then art:=TArtefact(GItem_Used)
  //else if (High(av) >= 1) and (av[1].VDW<>0) and (TObject(av[1].VDW) is TArtefact) then art:=TArtefact(av[1].VDW)
  //else exit;

  //if art.FItemType <> t_ArtMissileDef then exit;
  if Player = nil then Exit;

  if not Player.InNormalSpace then
  begin
    GR_SC.Play('Sound.NoMoney');
    MessageBoxGI(GFormShip, CTExt('FormShip.UseOnlyInSpace'), GIMB_Cancel or GIMB_IconInfo);
    exit;
  end;

  for i := 0 to Player.FCurStar.FMissile.Count - 1 do
    with TMissile(Player.FCurStar.FMissile.Items[i]) do
      if FFromShip = Player then FLive := 10000;

  MessageBoxGI(GFormShip, CTExt('FormShip.UseMissileDef'), GIMB_Cancel or GIMB_IconInfo);

end;

procedure SF_MessageBox(av:array of TVarEC; code:TCodeEC);
var flags:integer;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script MessageBox');
  if High(av) < 2 then flags:=GIMB_Cancel or GIMB_IconInfo else flags:=av[2].VInt;
  MessageBoxGI(GetCurrentML, av[1].VStr, flags);
end;

//GIMB_Ok=1;  ok button
//GIMB_Cancel=2; cancel button
//GIMB_IconInfo=4;       (i)
//GIMB_IconWarning=8;    (!)
//GIMB_IconQuestion=16;  (?)
//GIMB_IconError=32;     (x)
//GIMB_AlignLeft=64;   text align

procedure SF_MessageBoxYesNo(av:array of TVarEC; code:TCodeEC);
var flags:integer;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script MessageBoxYesNo');
  if High(av) < 2 then flags:=GIMB_Yes or GIMB_No or GIMB_IconQuestion else flags:=av[2].VInt or GIMB_Yes or GIMB_No;
  av[0].VInt := 0;
  if MessageBoxGI(GetCurrentML, av[1].VStr, flags) = GIMB_Yes then av[0].VInt := 1;
end;

procedure SF_CountBox(av:array of TVarEC; code:TCodeEC);
var
  cnt:integer;
  img,txt:WideString;
  zmin,zmax,zmaxok,zstep,price,cntmaxok,summaxok:integer;
begin
  if(High(av) < 4) then raise Exception.Create('Error.Script CountBox');
  //av[0].VInt := 0;
  img:= av[1].VStr;//'Bm.Items.2Minerals'
  txt:= av[2].VStr;
  zmin:=av[3].VInt;
  zmax:=av[4].VInt;

  if (High(av) > 4) then price:=av[5].VInt else price:=0;
  //if (High(av) > 5) then zstep:=av[6].VInt else zstep:=1; //doesn't work
  if (High(av) > 6) then zmaxok:=av[7].VInt else zmaxok:=zmax;
  if (High(av) > 7) then cntmaxok:=av[8].VInt else cntmaxok:=zmax;
  if (High(av) > 8) then summaxok:=av[9].VInt else summaxok:=MaxAllowedMoney;

  if (High(av) > 9) then cnt:=av[10].VInt else cnt:=zmin;
  if CountBox2(GetCurrentML, 'GI,'+av[1].VStr,av[2].VStr, zmin,zmax,zmaxok,price,cntmaxok,summaxok,cnt) = GIMB_Yes then av[0].VInt := cnt
  else av[0].VStr := 'Cancel';

end;

procedure SF_NumberBox(av:array of TVarEC; code:TCodeEC);
var
  cnt:Cardinal;
  img,units,txt:WideString;
  zmin,zmax,zmaxok,price,cntmaxok,summaxok:Cardinal;
begin
  if(High(av) < 4) then raise Exception.Create('Error.Script NumberBox');
  //av[0].VDW := 0;
  img:='GI,'+av[1].VStr;//'Bm.Items.2Minerals'
  txt:= av[2].VStr;
  zmin:=av[3].VDW;
  zmax:=av[4].VDW;
  if (High(av) > 4) then zmaxok:=av[5].VDW else zmaxok:=zmax;
  if (High(av) > 5) and (av[6].VStr<>'') then units:='GI,'+av[6].VStr else units:='';//'Bm.FormCount2.2Kind0'

  if (High(av) > 6) then cnt:=av[7].VInt else cnt:=zmin;

  if CountBox1(GetCurrentML, img, units, txt, zmin,zmax,zmaxok,cnt) = GIMB_Yes then av[0].VDW := cnt
  else av[0].VStr := 'Cancel';

end;

procedure SF_TextBox(av:array of TVarEC; code:TCodeEC);
var
  q_txt,a_txt:WideString;
  len:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script TextBox');
  q_txt:=av[1].VStr;
  a_txt:='';
  if(High(av) > 1) then a_txt:=av[2].VStr;
  len:=30;
  if(High(av) > 2) then len:=av[3].VInt;

  av[0].VStr := a_txt;
  if TextBox(GetCurrentML, q_txt, a_txt, len) = GIMB_Yes then av[0].VStr := a_txt;

end;

procedure SF_ListBox(av:array of TVarEC; code:TCodeEC);
var
  q_txt,s:WideString;
  a_list:TList;
  i:integer;
  pstr:PWideString;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ListBox');
  q_txt:=av[1].VStr;
  a_list:=TList.Create;
  i:=-1;

  if av[2].VType = vtArray then
  begin
    for i:=0 to av[2].VArray.Count-1 do
    begin
      new(pstr);
      pstr^:=TVarEC(av[2].VArray.Items[i]).VStr;
      a_list.Add(pstr);
      pstr:=nil;
    end;
  end else begin
    for i:=2 to High(av) do
    begin
      new(pstr);
      pstr^:=av[i].VStr;
      a_list.Add(pstr);
      pstr:=nil;
    end;
  end;

  if ListBox_Run(GetCurrentML, i, q_txt, a_list) = GIMB_Ok then av[0].VInt:=i else av[0].VInt:=-1;

  while a_list.Count > 0 do
  begin
    dispose(a_list.Items[0]);
    a_list.Delete(0);
  end;
  a_list.Free;

end;

procedure SF_FormCurShip(av:array of TVarEC; code:TCodeEC);
begin
  if      GetCurrentML = GFormHangar then av[0].VDW:= cardinal(GFormHangar.FSetShip)
  else if GetCurrentML = GFormScaner then av[0].VDW:= cardinal(GFormScaner.FShip)
  else if GetCurrentML = GFormShip   then av[0].VDW:= cardinal(GCurShip)
  else av[0].VDW:=0;
end;



procedure SF_UselessItemText(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
  txt:WideString;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script UselessItemText');
  obj:=TObject(av[1].VDW);
  item:=nil;
  txt:='';
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if(item <> nil) and (item is TUselessItem) then
  begin
    txt:=(item as TUselessItem).FCustomText;
    if(High(av) > 1) then (item as TUselessItem).FCustomText:=av[2].VStr;
  end;
  av[0].VStr:=txt;
end;

procedure SF_UselessItemData(av:array of TVarEC; code:TCodeEC);
var
  obj: TObject;
  item: TItem;
  data,no:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script UselessItemData');
  obj:=TObject(av[1].VDW);
  no:=av[2].VInt;
  item:=nil;
  data:=0;
  if(obj is TItem) then item:=TItem(obj);
  if(obj is TScriptItem) then item:=TScriptItem(obj).FItem;
  if(item <> nil) and (item is TUselessItem) and (no > 0) and (no <= 3) then
  begin
    data:=(item as TUselessItem).FData[no-1];
    if(High(av) > 2) then (item as TUselessItem).FData[no-1]:=av[3].VInt;
  end;
  av[0].VInt:=data;
end;


procedure SF_GetAchievementSHU(av:array of TVarEC; code:TCodeEC);
begin
GrantAchievement('SHU');
end;

procedure SF_GetAchievementGIRLSHIRE(av:array of TVarEC; code:TCodeEC);
begin
GrantAchievement('GIRLSHIRE');
end;

procedure SF_GetAchievementGIRLSQUEST(av:array of TVarEC; code:TCodeEC);
begin
GrantAchievement('GIRLSQUEST');
end;

procedure SF_GetAchievementPIRATEWIN(av:array of TVarEC; code:TCodeEC);
begin
GrantAchievement('PIRATEWIN');
end;

procedure SF_GetAchievementCOALLITION(av:array of TVarEC; code:TCodeEC);
begin
GrantAchievement('COALLITION');
end;

procedure SF_GetAchievementHULL(av:array of TVarEC; code:TCodeEC);
begin
GrantAchievement('HULL');
end;


procedure SF_UICheckElement(av:array of TVarEC; code:TCodeEC);
var formName,objName,checkType:WideString;
    ml:TMessageLoopGI;
    obj:TObjectGI;
begin
  if(High(av) < 3) then raise Exception.Create('Error.Script UICheckElement');
  formName:=av[1].VStr;//name of form
  //MainForm, PlanetQuest, GameLoad, GameSettings, Introduction, Hangar, Planet, PlanetNO, RuinsTalk, AB, Gov, Info, Rating, Rewards, Ship, Talk, Scaner, StarMap, Film, Galaxy, Jump, EquipmentShop, GoodsShop, SaveManager, GameMenu, CfgSettings, GameEnd, About, Score, SelectFace, Journal, LoadRobot, LoadQuest, LoadAB, Achievements

  objName:=av[2].VStr;//name of object in selected form (object must have name unique to selected form)
  obj:=nil;

  if formName='' then ml:=GetCurrentML
  else ml:=GetMLByName(formName);

  if ml<>nil then obj:=ml.GetByNameNE(objName);

  if obj=nil then raise Exception.Create('Error.Script UICheckElement - cant find '+objName+' ('+formName+')');

  checkType:=av[3].VStr;

  if checkType='IsActive' then
  begin
    av[0].VInt:=ord(obj.Active);
    exit;
  end;

  if checkType='PosX' then
  begin
    av[0].VInt:=obj.Pos.X;
    exit;
  end;

  if checkType='PosY' then
  begin
    av[0].VInt:=obj.Pos.Y;
    exit;
  end;

  if checkType='IsDisable' then
  begin
    if not (obj is TGraphButtonGI) then raise Exception.Create('Error.Script UICheckElement - '+objName+' ('+formName+') is not a button');
    av[0].VInt:=ord(TGraphButtonGI(obj).Disable);
    exit;
  end;

  if checkType='Text' then
  begin
    if obj is TEditGI then
    begin
      av[0].VStr:=TEditGI(obj).Text;
      if High(av) > 3 then TEditGI(obj).Text:=av[4].VStr;
    end
    else if obj is TLabelGI then av[0].VStr:=TLabelGI(obj).Text
    else raise Exception.Create('Error.Script UICheckElement - '+objName+' ('+formName+') is not a label or edit');
    exit;
  end;

  if checkType='Image' then
  begin
    if      obj is TgaiGI   then av[0].VStr:=TgaiGI(obj).Image
    else if obj is TgiGI    then av[0].VStr:=TgiGI(obj).Image
    else if obj is TImageGI then av[0].VStr:=TImageGI(obj).Image
    else raise Exception.Create('Error.Script UICheckElement - '+objName+' ('+formName+') is not a image');
    exit;
  end;

  if checkType='CurFrame' then
  begin
    if not (obj is TgaiGI) then raise Exception.Create('Error.Script UICheckElement - '+objName+' ('+formName+') is not a gai');
    av[0].VInt:=TgaiGI(obj).CurFrame;
    exit;
  end;

  if checkType='IsDown' then
  begin
    if obj is TGraphButtonGI then
    begin
      av[0].VInt:=ord(TGraphButtonGI(obj).Down);
      if High(av) > 3 then TGraphButtonGI(obj).Down:=(av[4].VInt<>0);
    end
    else raise Exception.Create('Error.Script UICheckElement - '+objName+' ('+formName+') is not a button');
    exit;
  end;

  raise Exception.Create('Error.Script UICheckElement - query not recognized - '+checkType);

end;


procedure SF_InterfaceState(av:array of TVarEC; code:TCodeEC);
var formName,objName:WideString;
    i:integer;
    intover:TInterfaceStateOverride;
    ml:TMessageLoopGI;
    obj:TObjectGI;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script InterfaceState');
  formName:=av[1].VStr;//name of form
  //MainForm, PlanetQuest, GameLoad, GameSettings, Introduction, Hangar, Planet, PlanetNO, RuinsTalk, AB, Gov, Info, Rating, Rewards, Ship, Talk, Scaner, StarMap, Film, Galaxy, Jump, EquipmentShop, GoodsShop, SaveManager, GameMenu, CfgSettings, GameEnd, About, Score, SelectFace, Journal, LoadRobot, LoadQuest, LoadAB, Achievements

  objName:=av[2].VStr;//name of object in selected form (object must have name unique to selected form)

  if Galaxy=nil then
  begin
    ml:=GetMLByName(formName);
    if ml=nil then raise Exception.Create('ML not found - '+formName);
    obj:=ml.GetByNameNE(objName);
    if obj=nil then begin SFT('Object not found - '+objName); exit; end;
    av[0].VInt:=ord(obj.Active);
    if (obj is TGraphButtonGI) and TGraphButtonGI(obj).Disable and obj.Active then av[0].VInt:=2;

    if High(av) > 2 then
    begin
      obj.Active:=av[3].VInt>0;
      if (av[3].VInt>1) and (obj is TGraphButtonGI) then TGraphButtonGI(obj).Disable := av[3].VInt=2;
    end;

    exit;
  end;
  
  for i:=0 to Galaxy.FInterfaceStateOverrides.Count-1 do
  begin
    intover:=Galaxy.FInterfaceStateOverrides.Items[i];
    if intover.FMLName<>formName then continue;
    if intover.FGIName<>objName then continue;
    av[0].VInt:=ord(intover.State);
    if High(av) > 2 then
    begin
      if av[3].VInt<0 then
      begin
        Galaxy.FInterfaceStateOverrides.Delete(i);
        intover.Free;
      end else intover.State:=av[3].VInt;
    end;
    exit;
  end;
  av[0].VInt:=-1;
  if (High(av) > 2) and (av[3].VInt>=0) then
  begin
    intover:=TInterfaceStateOverride.Create();
    Galaxy.FInterfaceStateOverrides.Add(intover);
    intover.Init(formName,objName,av[3].VInt);
  end;

  //returns: -1 - override does not exist, 0 - override hides object, 1 - override shows object
  //if 3rd argument present: -1 delete override (return object to normal state), 0 - hide object, 1 - show object
  //does NOT prevent main code from changing object state and is not even aware if that happens (so don't use on objects that are switched on/off by main code)
  //will crash if can't find form or object inside it
end;


procedure SF_InterfaceText(av:array of TVarEC; code:TCodeEC);
var formName,objName:WideString;
    i:integer;
    intover:TInterfaceTextOverride;
    ml:TMessageLoopGI;
    obj:TObjectGI;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script InterfaceText');
  formName:=av[1].VStr;//name of form

  objName:=av[2].VStr;//name of object in selected form (object must have name unique to selected form)
  //must be of type Label

  if Galaxy=nil then
  begin
    ml:=GetMLByName(formName);
    if ml=nil then raise Exception.Create('ML not found - '+formName);
    obj:=ml.GetByNameNE(objName);
    if obj=nil then begin SFT('Object not found - '+objName); exit; end;
    if not (obj is TLabelGI) then raise Exception.Create('Object is not a label - '+objName);

    av[0].VStr:=TLabelGI(obj).Text;
    if High(av) > 2 then TLabelGI(obj).Text:=av[3].VStr;
    exit;
  end;

  for i:=0 to Galaxy.FInterfaceTextOverrides.Count-1 do
  begin
    intover:=Galaxy.FInterfaceTextOverrides.Items[i];
    if intover.FMLName<>formName then continue;
    if intover.FGIName<>objName then continue;
    av[0].VStr:=intover.Text;
    if High(av) > 2 then
    begin
      if av[3].VStr='' then
      begin
        Galaxy.FInterfaceTextOverrides.Delete(i);
        intover.Free;
      end else intover.Text:=av[3].VStr;
    end;
    exit;
  end;
  av[0].VStr:='';
  if (High(av) > 2) and (av[3].VStr<>'') then
  begin
    intover:=TInterfaceTextOverride.Create();
    Galaxy.FInterfaceTextOverrides.Add(intover);
    intover.Init(formName,objName,av[3].VStr);
  end;

end;

procedure SF_InterfaceImage(av:array of TVarEC; code:TCodeEC);
var formName,objName:WideString;
    i:integer;
    intover:TInterfaceImageOverride;
    ml:TMessageLoopGI;
    obj:TObjectGI;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script InterfaceImage');
  formName:=av[1].VStr;//name of form

  objName:=av[2].VStr;//name of object in selected form (object must have name unique to selected form)
  //must be of type GI, GAI, or Image

  if Galaxy=nil then
  begin
    ml:=GetMLByName(formName);
    if ml=nil then raise Exception.Create('ML not found - '+formName);
    obj:=ml.GetByNameNE(objName);
    if obj=nil then begin SFT('Object not found - '+objName); exit; end;

    if obj is TgaiGI then av[0].VStr:=TgaiGI(obj).Image
    else if obj is TgiGI then av[0].VStr:=TgiGI(obj).Image
    else if obj is TImageGI then av[0].VStr:=TImageGI(obj).Image
    else av[0].VStr:=obj.Style;
    //raise Exception.Create('Object is not an image - '+objName);

    if High(av) > 2 then
    begin
      if (GetCountParEC(av[3].VStr,':')>1) and (GetStrParEC(av[3].VStr,0,':')='Style') then obj.Style:=GetStrParEC(av[3].VStr,1,':')
      else if obj is TgaiGI then TgaiGI(obj).Image:=av[3].VStr
      else if obj is TgiGI then TgiGI(obj).Image:=av[3].VStr
      else if obj is TImageGI then TImageGI(obj).Image:=av[3].VStr
      else raise Exception.Create('Object is not an image - '+objName);
    end;

    exit;
  end;
  
  for i:=0 to Galaxy.FInterfaceImageOverrides.Count-1 do
  begin
    intover:=Galaxy.FInterfaceImageOverrides.Items[i];
    if intover.FMLName<>formName then continue;
    if intover.FGIName<>objName then continue;
    av[0].VStr:=intover.Image;
    if High(av) > 2 then
    begin
      if av[3].VStr='' then
      begin
        Galaxy.FInterfaceImageOverrides.Delete(i);
        intover.Free;
      end else intover.Image:=av[3].VStr;
    end;
    exit;
  end;
  av[0].VStr:='';
  if (High(av) > 2) and (av[3].VStr<>'') then
  begin
    intover:=TInterfaceImageOverride.Create();
    Galaxy.FInterfaceImageOverrides.Add(intover);
    intover.Init(formName,objName,av[3].VStr);
  end;

end;

procedure SF_InterfacePos(av:array of TVarEC; code:TCodeEC);
var formName,objName:WideString;
    i,deltax,deltay,deltaz:integer;
    intover:TInterfacePosOverride;
    ml:TMessageLoopGI;
    obj:TObjectGI;
begin
  if(High(av) < 5) then raise Exception.Create('Error.Script InterfacePos');
  formName:=av[1].VStr;//name of form

  objName:=av[2].VStr;//name of object in selected form (object must have name unique to selected form)

  deltax:=av[3].VInt;
  deltay:=av[4].VInt;
  deltaz:=av[5].VInt;

  if Galaxy=nil then
  begin
    ml:=GetMLByName(formName);
    if ml=nil then raise Exception.Create('ML not found - '+formName);
    obj:=ml.GetByNameNE(objName);
    if obj=nil then begin SFT('Object not found - '+objName); exit; end;

    obj.Pos:=Point(deltax,deltay);
    obj.PosZd:=deltaz;
    exit;
  end;
  
  for i:=0 to Galaxy.FInterfacePosOverrides.Count-1 do
  begin
    intover:=Galaxy.FInterfacePosOverrides.Items[i];
    if intover.FMLName<>formName then continue;
    if intover.FGIName<>objName then continue;

    if (deltax=0) and (deltay=0) and (deltaz=0) then
    begin
      Galaxy.FInterfacePosOverrides.Delete(i);
      intover.Free;
    end else intover.SetPos(deltax,deltay,deltaz);
    exit;
  end;

  if (deltax<>0) or (deltay<>0) or (deltaz<>0) then
  begin
    intover:=TInterfacePosOverride.Create();
    Galaxy.FInterfacePosOverrides.Add(intover);
    intover.Init(formName,objName,deltax,deltay,deltaz);
  end;

end;

procedure SF_InterfaceSize(av:array of TVarEC; code:TCodeEC);
var formName,objName:WideString;
    i,sizex,sizey:integer;
    intover:TInterfaceSizeOverride;
    ml:TMessageLoopGI;
    obj:TObjectGI;
begin
  if(High(av) < 4) then raise Exception.Create('Error.Script InterfaceSize');
  formName:=av[1].VStr;//name of form

  objName:=av[2].VStr;//name of object in selected form (object must have name unique to selected form)

  sizex:=av[3].VInt;
  sizey:=av[4].VInt;

  if Galaxy=nil then
  begin
    ml:=GetMLByName(formName);
    if ml=nil then raise Exception.Create('ML not found - '+formName);
    obj:=ml.GetByNameNE(objName);
    if obj=nil then begin SFT('Object not found - '+objName); exit; end;

    obj.Size:=Point(sizex,sizey);
    exit;
  end;

  for i:=0 to Galaxy.FInterfaceSizeOverrides.Count-1 do
  begin
    intover:=Galaxy.FInterfaceSizeOverrides.Items[i];
    if intover.FMLName<>formName then continue;
    if intover.FGIName<>objName then continue;

    if (sizex=0) and (sizey=0) then
    begin
      Galaxy.FInterfaceSizeOverrides.Delete(i);
      intover.Free;
    end else intover.SetSize(sizex,sizey);
    exit;
  end;

  if (sizex<>0) or (sizey<>0) then
  begin
    intover:=TInterfaceSizeOverride.Create();
    Galaxy.FInterfaceSizeOverrides.Add(intover);
    intover.Init(formName,objName,sizex,sizey);
  end;

end;


procedure SF_ButtonClick(av:array of TVarEC; code:TCodeEC);
var formName,objName:WideString;
    obj:TObjectGI;
    ml:TMessageLoopGI;
    but:TGraphButtonGI;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script ButtonClick');
  formName:=av[1].VStr;//name of form
  objName:=av[2].VStr;//name of object in selected form (object must have name unique to selected form)

  if formName='' then ml:=GetCurrentML
  else ml:=GetMLByName(formName);

  if ml=nil then raise Exception.Create('Error.Script ButtonClick - ML not found');

  obj:=ml.GetByNameNE(objName);
  if obj=nil then raise Exception.Create('Error.Script ButtonClick - Object not found');

  if not (obj is TGraphButtonGI) then raise Exception.Create('Error.Script ButtonClick - Object not a button');

  but:=obj as TGraphButtonGI;

  if Assigned(but.FunButtonUp) then but.FunButtonUp(but)
  else if Assigned(but.FunButtonDown) then but.FunButtonDown(but);

end;


procedure SF_SetFocus(av:array of TVarEC; code:TCodeEC);
var formName,objName:WideString;
    obj:TObjectGI;
    ml:TMessageLoopGI;
    but:TGraphButtonGI;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SetFocus');
  formName:=av[1].VStr;//name of form
  objName:=av[2].VStr;//name of object in selected form (object must have name unique to selected form)

  if formName='' then ml:=GetCurrentML
  else ml:=GetMLByName(formName);

  if ml=nil then raise Exception.Create('Error.Script SetFocus - ML not found');

  obj:=ml.GetByNameNE(objName);
  if obj=nil then raise Exception.Create('Error.Script SetFocus - Object not found');

  ml.SetFocus(obj);

end;


procedure SF_FormShipCurItem(av:array of TVarEC; code:TCodeEC);
var
  actionType:integer;
begin
  if GetCurrentML <> GFormShip then raise Exception.Create('Error.Script FormShipCurItem');

  with GFormShip do
  begin
    if High(av) < 1 then
    begin
      av[0].VDW := Cardinal(FMoveItem);
      exit;
    end;

    if av[1].VType = vtStr then
    begin
      if av[1].VStr='MoveType' then actionType:=0 //check what we are moving: 0 - nothing, 1 - stackable, 2 - equipment, 3 - artefact
      else if av[1].VStr='StackableType' then actionType:=1 //only for stackable
      else if av[1].VStr='StackableCount' then actionType:=2 //goods dont have item object so must check this way
      else if av[1].VStr='StackableCost' then actionType:=3 // -/-
      else if av[1].VStr='PutBack' then actionType:=4 //return item to its place
      else if av[1].VStr='Destroy' then actionType:=5 //free item
      else if av[1].VStr='Detach' then actionType:=6 //clear hand but dont destroy item (script have to put it somewhere)
      else raise Exception.Create('Error.Script FormShipCurItem - query not recognized: '+av[1].VStr);
    end else begin
      actionType:=av[3].VInt;
    end;

    case actionType of
      0: av[0].VInt:=FMoveType;
      1: av[0].VInt:=ord(FMoveItemType);
      2: av[0].VInt:=FMoveCnt;
      3: av[0].VInt:=FMoveCost;
      4: SlotCancel;
      5: begin
           if FMoveItem<>nil then FMoveItem.Free;
           FMoveItem:=nil;
           FMoveType:=0;
           GCurShip.CalcParam;
           if not IsDefaultCursor('Main') then SetDefaultCursor('Main');
           Update;
         end;
      6: begin
           av[0].VDW:=Cardinal(FMoveItem);
           FMoveItem:=nil;
           FMoveType:=0;
           GCurShip.CalcParam;
           if not IsDefaultCursor('Main') then SetDefaultCursor('Main');
           Update;
         end;
      else Exception.Create('Error.Script FormShipCurItem - query not recognized: '+inttostrEC(actionType));
    end;
  end;
end;


procedure SF_UpdateFormShip(av:array of TVarEC; code:TCodeEC);
begin
  if GetCurrentML = GFormShip then with GFormShip do
  begin
    FCriticalUpdate := true;
    FReenter := true;
    SoundOpenClose := false;
    ButtonExit(nil);
  end;
end;

procedure SF_CurrentForm(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VStr:=GetCurrentML.FName;
end;


procedure SF_FormChange(av:array of TVarEC; code:TCodeEC);
var form:mlForm;
    mlName:WideString;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script FormChange');
  mlName:=av[1].VStr;

  for form:=Low(form) to High(form) do
  begin
    if GForm[form]=nil then continue;
    if not (GForm[form] is TMessageLoopGI) then continue;
    if (GForm[form] as TMessageLoopGI).FName<>mlName then continue;
    GFormNext:=form;
    if (GForm[form] = GFormShip) then
    begin
      if (High(av)>=2) then GFormShip.FSetShip:=TShip(av[2].VDW);
      GFormShip2_Return:=GFormCur;//FormToId(GetCurrentML);

      if (GFormCur=mlf_StarMap) or not(GForm[GFormCur] is TMessageLoopGIWithMainPanel) or (TMessageLoopGIWithMainPanel(GForm[GFormCur]).FPanelMain=nil) then
      begin
        GFormShip2_Return:=GFormCur;
        GetCurrentML.ExitLoop;
        exit;
      end;

      TMessageLoopGIWithMainPanel(GForm[GFormCur]).FPanelMain.Ship(nil);
      exit;
    end;
    GetCurrentML.ExitLoop;

    exit;
  end;

  raise Exception.Create('Error.Script FormChange - ML not found');

end;

procedure SF_RunChildForm(av:array of TVarEC; code:TCodeEC);
var form:mlForm;
    mlName:WideString;
    parent,parent2,child:TMessageLoopGI;
    buf,buf2:TObjectGI;
    cs:TCursorStateGI;
    //i:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script RunChildForm');
  mlName:=av[1].VStr;

  for form:=Low(form) to High(form) do
  begin

    if GForm[form]=nil then continue;
    if not (GForm[form] is TMessageLoopGI) then continue;
    if (GForm[form] as TMessageLoopGI).FName<>mlName then continue;
    child:=TMessageLoopGI(GForm[form]);
    parent:=GetCurrentML;

    buf2:=nil;
    buf:=child.GetByNameNE('BGBuf');
    if buf<>nil then
    begin
      GR_BGBuf_Load;
      (buf as TGraphBufGI).CreateExt(GR_BGBuf);
    end else begin
      buf2:=child.GetByNameNE('BGBufChild');
      if buf2<>nil then
      begin
        GR_BGBuf_Load;
        (buf2 as TGraphBufGI).CreateExt(GR_BGBuf);
        buf2.Active:=true;
      end;
    end;

    parent.SysObj.Msg_DeActivateEx;
    parent.GetCursor(@cs);
    parent.ShowCursor:=False;
    parent.Draw;

    child.FParentML:=parent;
    parent.FChildML:=child;

    if (child = GFormGalaxy) and (High(av)>=2) then GFormGalaxy.FMode:=fGalaxyMode(av[2].VInt);//fgm_Teleport,fgm_Show,fgm_Move,fgm_BlackHole

    if child.Run=1 then av[0].VInt:=1 else av[0].VInt:=0;

    if buf2<>nil then buf2.Active:=false;

    child.FParentML:=nil;
    parent.FChildML:=nil;

    if ((buf<>nil) or (buf2<>nil)) and (parent.FParentML<>nil) then
    begin
      parent2:=parent.FParentML;
      while parent2.FParentML<>nil do parent2:=parent2.FParentML;
      GR_NeedFullRedraw:=true;
		  parent2.Draw2;
      {for i:=0 to 2 do
      begin
        GR_DrawScreen();
        parent2.DrawAll;
      end;}
      GR_BGBuf_Load;
    end;

    parent.RU_AddAll;
    parent.SetCursor(@cs);
    parent.SynchronizeCursor;
    parent.SysObj.Msg_ActivateEx;
    parent.DrawAll;



    GR_MouseMoveSend();

    exit;
  end;

  raise Exception.Create('Error.Script RunChildForm - ML not found');

end;

procedure SF_OpenCustomForm(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script OpenCustomForm');
  av[0].VInt:=RunCustomForm(GetCurrentML,av[1].VStr); //path in ML, loads script code from CodeBeforeRun and CodeAfterRun
end;

procedure SF_CloseCustomForm(av:array of TVarEC; code:TCodeEC);
var res:integer;
begin
  if GFormCustom=nil then raise Exception.Create('Error.Script CloseCustomForm - no custom form');
  if High(av) > 0 then res:=av[1].VInt else res:=1;//0 - no exit, 255 - parent form closed
  GFormCustom.ExitLoop(res);
end;


procedure SF_CustomInterfaceState(av:array of TVarEC; code:TCodeEC);
var obj:TObjectGI;
    ml:TMessageLoopGI;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script CustomInterfaceState');
  ml:=GFormCustom;
  if ml=nil then raise Exception.Create('Error.Script CustomInterfaceState - no custom form');
  obj:=ml.GetByNameNE(av[1].VStr);
  if obj=nil then raise Exception.Create('Error.Script CustomInterfaceState - object not found');
  av[0].VInt:=ord(obj.Active);
  if High(av) > 1 then obj.Active:=(av[2].VInt>0);

  if obj is TGraphButtonGI then
  begin
    if obj.Active then av[0].VInt:=av[0].VInt+ord(TGraphButtonGI(obj).Disable);
    if High(av) > 1 then TGraphButtonGI(obj).Disable:=(av[2].VInt=2);
  end;
end;

procedure SF_CustomInterfaceText(av:array of TVarEC; code:TCodeEC);
var obj:TObjectGI;
    ml:TMessageLoopGI;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script CustomInterfaceText');
  ml:=GFormCustom;
  if ml=nil then raise Exception.Create('Error.Script CustomInterfaceText - no custom form');
  obj:=ml.GetByNameNE(av[1].VStr);
  if obj=nil then raise Exception.Create('Error.Script CustomInterfaceText - object not found: '+av[1].VStr);

  if obj is TLabelGI then av[0].VStr:=TLabelGI(obj).Text
  else if obj is TEditGI then av[0].VStr:=TEditGI(obj).Text
  else raise Exception.Create('Error.Script CustomInterfaceText - object is not a label or edit: '+av[1].VStr);

  if High(av) > 1 then
  begin
    if obj is TLabelGI then TLabelGI(obj).Text:=av[2].VStr
    else if obj is TEditGI then TEditGI(obj).Text:=av[2].VStr;
  end;
end;

procedure SF_CustomInterfaceImage(av:array of TVarEC; code:TCodeEC);
var obj:TObjectGI;
    ml:TMessageLoopGI;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script CustomInterfaceImage');
  ml:=GFormCustom;
  if ml=nil then raise Exception.Create('Error.Script CustomInterfaceImage - no custom form');
  obj:=ml.GetByNameNE(av[1].VStr);
  if obj=nil then raise Exception.Create('Error.Script CustomInterfaceImage - object not found: '+av[1].VStr);

  if obj is TgaiGI then av[0].VStr:=TgaiGI(obj).Image
  else if obj is TgiGI then av[0].VStr:=TgiGI(obj).Image
  else if obj is TImageGI then av[0].VStr:=TImageGI(obj).Image
  else av[0].VStr:=obj.Style;
  //else raise Exception.Create('Error.Script CustomInterfaceImage - object is not a image: '+av[1].VStr);

  if High(av) > 1 then
  begin
    if (GetCountParEC(av[2].VStr,':')>1) and (GetStrParEC(av[2].VStr,0,':')='Style') then obj.Style:=GetStrParEC(av[2].VStr,1,':')
    else if obj is TgaiGI then TgaiGI(obj).Image:=av[2].VStr
    else if obj is TgiGI then TgiGI(obj).Image:=av[2].VStr
    else if obj is TImageGI then TImageGI(obj).Image:=av[2].VStr
    else raise Exception.Create('Error.Script CustomInterfaceImage - object is not a image: '+av[1].VStr);
  end;

end;


procedure SF_CustomInterfacePos(av:array of TVarEC; code:TCodeEC);
var obj:TObjectGI;
    ml:TMessageLoopGI;
begin
  if High(av) < 3 then raise Exception.Create('Error.Script CustomInterfacePos');
  ml:=GFormCustom;
  if ml=nil then raise Exception.Create('Error.Script CustomInterfacePos - no custom form');
  obj:=ml.GetByNameNE(av[1].VStr);
  if obj=nil then raise Exception.Create('Error.Script CustomInterfacePos - object not found');
  obj.Pos:=Point(av[2].VInt,av[3].VInt);
end;

procedure SF_CustomInterfacePosZ(av:array of TVarEC; code:TCodeEC);
var obj:TObjectGI;
    ml:TMessageLoopGI;
begin
  if High(av) < 2 then raise Exception.Create('Error.Script CustomInterfacePosZ');
  ml:=GFormCustom;
  if ml=nil then raise Exception.Create('Error.Script CustomInterfacePosZ - no custom form');
  obj:=ml.GetByNameNE(av[1].VStr);
  if obj=nil then raise Exception.Create('Error.Script CustomInterfacePosZ - object not found');
  obj.PosZd:=av[2].VInt;
end;

procedure SF_CustomInterfaceSize(av:array of TVarEC; code:TCodeEC);
var obj:TObjectGI;
    ml:TMessageLoopGI;
begin
  if High(av) < 3 then raise Exception.Create('Error.Script CustomInterfacePos');
  ml:=GFormCustom;
  if ml=nil then raise Exception.Create('Error.Script CustomInterfacePos - no custom form');
  obj:=ml.GetByNameNE(av[1].VStr);
  if obj=nil then raise Exception.Create('Error.Script CustomInterfacePos - object not found');
  obj.Size:=Point(av[2].VInt,av[3].VInt);
end;


procedure SF_StarMapCenterView(av:array of TVarEC; code:TCodeEC);
var pos:TPos;
    i,circles:integer;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script StarMapCenterView');
  if GForm[GFormCur]<>GFormStarMap then exit;
  pos.X:=av[1].VInt;
  pos.Y:=av[2].VInt;
  GFormStarMap.PosView:=DxyToPoint(pos);

  if (High(av) > 2) then circles:=av[3].VInt else circles:=0;
  for i:=0 to circles-1 do GFormStarMap.PlayIAnim(pos,'Bm.SI.'+VideoModeStr+'Ring',i*200);
end;

procedure SF_StarMapCurPosX(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=GFormStarMap.PosView.X;
end;

procedure SF_StarMapCurPosY(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VInt:=GFormStarMap.PosView.Y;
end;


procedure SF_CustomWeaponTypes(av:array of TVarEC; code:TCodeEC);
var no:integer;
begin
  if High(av) < 1 then
  begin
    av[0].VInt:=Galaxy.FCustomWeaponInfos.Count;
    exit;
  end;
  no:=av[1].VInt;
  if (no >= 0) and (no < Galaxy.FCustomWeaponInfos.Count) then av[0].VStr:=PWeaponInfo(Galaxy.FCustomWeaponInfos[no]).SysName
  else av[0].VStr:='';
end;


procedure SF_InventNewCustomWeapon(av:array of TVarEC; code:TCodeEC);
var winfo,winfofrom:PWeaponInfo;
    typefrom:TItemType;
    i:integer;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script InventNewCustomWeapon');
  winfo:=Galaxy.AddCustomWeaponInfo(av[1].VStr);
  av[0].VDW:=Cardinal(winfo);
  if High(av) > 1 then typefrom:=TItemType(av[2].VInt) else typefrom:=BasicWeapon;//takes t_WeaponN as argument
  if not(typefrom in HardCodedWeapons) then raise Exception.Create('Error.Script InventNewCustomWeapon - invalid type '+av[2].VStr);//typefrom:=BasicWeapon;
  winfofrom:=@mWeapon[typefrom];

  winfo.TechLevel:=winfofrom.TechLevel;
  winfo.TechRadius:=winfofrom.TechRadius;
  winfo.kCost:=winfofrom.kCost;
  winfo.MinDamage:=winfofrom.MinDamage;
  winfo.MaxDamage:=winfofrom.MaxDamage;
  winfo.AverageSize:=winfofrom.AverageSize;
  winfo.AverageRadius:=winfofrom.AverageRadius;
  winfo.Speed:=winfofrom.Speed;
  winfo.MissileRadius:=winfofrom.MissileRadius;
  winfo.MissileMaxSpeed:=winfofrom.MissileMaxSpeed;
  winfo.MissileMinSpeed:=winfofrom.MissileMinSpeed;
  winfo.MissileChanceToBeHit:=winfofrom.MissileChanceToBeHit;
  winfo.DamageType:=winfofrom.DamageType;
  winfo.ShotType:=winfofrom.ShotType;
  winfo.ShotCount:=winfofrom.ShotCount;
  winfo.AttackCount:=winfofrom.AttackCount;
  winfo.SecondaryDamageRadius:=winfofrom.SecondaryDamageRadius;
  winfo.MiningFactor:=winfofrom.MiningFactor;
  winfo.PrimarySE:=winfofrom.PrimarySE;
  winfo.SecondarySE:=winfofrom.SecondarySE;
  winfo.AreaSE:=winfofrom.AreaSE;
  winfo.DefaultPalette:=winfofrom.DefaultPalette;
  winfo.Availability:=winfofrom.Availability;
  winfo.ABWeaponType:=winfofrom.ABWeaponType;

  for i:=low(TTechLevel) to high(TTechLevel) do winfo.mWeaponDamage[i]:=winfofrom.mWeaponDamage[i];

end;

procedure SF_GetCustomWeaponInfo(av:array of TVarEC; code:TCodeEC);
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script GetCustomWeaponInfo');
  av[0].VDW:=Cardinal(Galaxy.GetCustomWeaponInfo(av[1].VStr));
end;

procedure SF_GetCustomWeaponData(av:array of TVarEC; code:TCodeEC);
var winfo:PWeaponInfo;
    stat:WideString;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script GetCustomWeaponStats');

  if av[1].VType = vtStr then winfo:=Galaxy.GetCustomWeaponInfo(av[1].VStr)
  else winfo:=@(mWeapon[TItemType(av[1].VInt)]);
  
  stat:=av[2].Vstr;

  if stat='TechLevel' then av[0].VInt:=winfo.TechLevel
  else if stat='AverageSize' then av[0].VInt:=winfo.AverageSize
  else if stat='AverageRadius' then av[0].VInt:=winfo.AverageRadius
  else if stat='MissileRadius' then av[0].VInt:=winfo.MissileRadius
  else if stat='SecondaryDamageRadius' then av[0].VFloat:=winfo.SecondaryDamageRadius
  else if stat='MaxDamage' then av[0].VInt:=winfo.MaxDamage
  else if stat='MinDamage' then av[0].VInt:=winfo.MinDamage
  else if stat='DamageType' then av[0].VDW:=Cardinal(winfo.DamageType)
  else if stat='kCost' then av[0].VFloat:=winfo.kCost
  else if stat='AttackCount' then av[0].VInt:=winfo.AttackCount
  else if stat='ShotCount' then av[0].VInt:=winfo.ShotCount
  else if stat='ShotType' then
  begin
    case winfo.ShotType of
      shtNormal: av[0].VStr:='Normal';
      shtSplash: av[0].VStr:='Splash';
      shtExploder: av[0].VStr:='Exploder';
      shtAreaDamage: av[0].VStr:='AreaDamage';
      shtTorpedo: av[0].VStr:='Torpedo';
      shtMissile: av[0].VStr:='Missile';
      shtRocket: av[0].VStr:='Rocket';
      shtChain: av[0].VStr:='Chain';
    end;
    //if winfo.ShotType in [shtMissile,shtRocket,shtChain] then av[0].VStr:=av[0].VStr+inttostrEC(winfo.ShotCount);
  end
  else if stat='Availability' then
  begin
    case winfo.Availability of
      avFree: av[0].VStr:='Free';
      avCoalitionOnly: av[0].VStr:='CoalitionOnly';
      avPirateOnly: av[0].VStr:='PirateOnly';
      avNotSold: av[0].VStr:='NotSold';
      avNotSoldAndNodeRepair: av[0].VStr:='NotSoldAndNodeRepair';
      avMalocOnly: av[0].VStr:='MalocOnly';
      avPelengOnly: av[0].VStr:='PelengOnly';
      avPeopleOnly: av[0].VStr:='PeopleOnly';
      avFeiOnly: av[0].VStr:='FeiOnly';
      avGaalOnly: av[0].VStr:='GaalOnly';
      else raise Exception.Create('Error.Script GetCustomWeaponStats - unknown availability type');
    end;
  end
  else raise Exception.Create('Error.Script GetCustomWeaponStats - unknown stat '+stat);
end;

procedure SF_GetCustomWeaponPrimaryDamageType(av:array of TVarEC; code:TCodeEC);
var winfo:PWeaponInfo;
begin
  if(High(av) < 1) then raise Exception.Create('Error.Script GetCustomWeaponPrimaryDamageType');
  if av[1].VType = vtStr then winfo:=Galaxy.GetCustomWeaponInfo(av[1].VStr)
  else winfo:=@(mWeapon[TItemType(av[1].VInt)]);
  av[0].VInt:=integer(PrimaryDamageType(winfo.DamageType));
end;

procedure SF_SetCustomWeaponAvailability(av:array of TVarEC; code:TCodeEC);
var winfo:PWeaponInfo;
    tstr:WideString;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SetCustomWeaponAvailability');
  winfo:=PWeaponInfo(av[1].VDW);
  av[0].VDW:=Cardinal(winfo);

  tstr:=av[2].VStr;

  if tstr='Free' then winfo.Availability:=avFree //weapon can be sold in all coalition and pirate systems
  else if tstr='CoalitionOnly' then winfo.Availability:=avCoalitionOnly //only for coalition systems (and will not be sold to pirates unless option of buying from player shop is selected)
  else if tstr='PirateOnly' then winfo.Availability:=avPirateOnly //only for coalition systems (and will not be sold to transports and military unless option of buying from player shop is selected)
  else if tstr='NotSold' then winfo.Availability:=avNotSold //weapon never appears in shops
  else if tstr='NotSoldAndNodeRepair' then winfo.Availability:=avNotSoldAndNodeRepair //weapon never appears in shops and require nodes to repair
  else if tstr='MalocOnly' then winfo.Availability:=avMalocOnly
  else if tstr='PelengOnly' then winfo.Availability:=avPelengOnly
  else if tstr='PeopleOnly' then winfo.Availability:=avPeopleOnly
  else if tstr='FeiOnly' then winfo.Availability:=avFeiOnly
  else if tstr='GaalOnly' then winfo.Availability:=avGaalOnly
  else winfo.Availability:=avFree;
end;

procedure SF_SetCustomWeaponPrimaryData(av:array of TVarEC; code:TCodeEC);
var winfo:PWeaponInfo;
begin
  if(High(av) < 4) then raise Exception.Create('Error.Script SetCustomWeaponPrimaryData');
  winfo:=PWeaponInfo(av[1].VDW);
  av[0].VDW:=Cardinal(winfo);

  winfo.TechLevel:=av[2].VInt;//1..8
  winfo.TechRadius:=mWeapon[TItemType(av[3].VInt)].TechRadius;//t_Weapon1..t_Weapon12 only (which planetary invention level will be used)
  winfo.ABWeaponType:=TItemType(av[4].VInt);//t_Weapon1..t_Weapon18 for AB
end;

procedure SF_SetCustomWeaponSizeAndCost(av:array of TVarEC; code:TCodeEC);
var winfo:PWeaponInfo;
begin
  if(High(av) < 3) then raise Exception.Create('Error.Script SetCustomWeaponSizeAndCost');
  winfo:=PWeaponInfo(av[1].VDW);
  av[0].VDW:=Cardinal(winfo);

  winfo.kCost:=av[2].VFloat;
  winfo.AverageSize:=av[3].VInt;
end;

procedure SF_SetCustomWeaponDamageData(av:array of TVarEC; code:TCodeEC);
var winfo:PWeaponInfo;
    dt:TDamageType;
    dtype:TSetDamageType;
    i,cnt:integer;
    tstr:WideString;
begin
  if(High(av) < 4) then raise Exception.Create('Error.Script SetCustomWeaponDamageData');
  winfo:=PWeaponInfo(av[1].VDW);
  av[0].VDW:=Cardinal(winfo);

  winfo.MinDamage:=av[2].VInt;
  winfo.MaxDamage:=av[3].VInt;

  dtype:=[];

  if av[4].VType = vtStr then
  begin
    tstr:=','+av[4].VStr+',';//string list of damage types
    for dt:=low(dt) to high(dt) do
      if Pos(','+DamageTypeSysName[dt]+',',tstr)>0 then include(dtype,dt);

  end else begin
    dtype:=TSetDamageType(Cardinal(av[4].VDW));//or numeric set of damage types

  end;

  winfo.DamageType:=dtype;

  if (High(av)>4) and (av[5].VType = vtStr) then
  begin
    tstr:=av[5].VStr;
    cnt:=GetCountParEC(tstr,',');
    for i:=1 to min(CntTechLevel,cnt) do winfo.mWeaponDamage[i]:=strtofloatEC(GetStrParEC(tstr,i-1,','));
  end
  else
  for i:=1 to min(CntTechLevel,High(av)-4) do
  begin
    if (av[4+i].VType in [vtInt,vtDW]) and (av[4+i].VInt=0) then continue;
    winfo.mWeaponDamage[i]:=av[4+i].VFloat;
  end;
end;

procedure SF_SetCustomWeaponShotData(av:array of TVarEC; code:TCodeEC);
var winfo:PWeaponInfo;
    dt:Cardinal;
    dtype:TSetDamageType;
    sht:WideString;
begin
  if(High(av) < 2) then raise Exception.Create('Error.Script SetCustomWeaponShotData');
  winfo:=PWeaponInfo(av[1].VDW);
  av[0].VDW:=Cardinal(winfo);

  sht:=av[2].VStr;
  winfo.ShotType:=shtNormal;
  winfo.ShotCount:=1;

  if (Pos('Normal', sht) > 0) then begin end
  else if (Pos('Splash', sht) > 0) then winfo.ShotType:=shtSplash
  else if (Pos('Exploder', sht) > 0) then winfo.ShotType:=shtExploder
  else if (Pos('AreaDamage', sht) > 0) then winfo.ShotType:=shtAreaDamage
  else if (Pos('Torpedo', sht) > 0) then winfo.ShotType:=shtTorpedo
  else if (Pos('Missile', sht) > 0) then winfo.ShotType:=shtMissile
  else if (Pos('Rocket', sht) > 0) then winfo.ShotType:=shtRocket
  else if (Pos('Chain', sht) > 0) then winfo.ShotType:=shtChain;

  if winfo.ShotType in [shtRocket,shtMissile,shtChain] then winfo.ShotCount:=StrToIntEC(sht);//example: 'Rocket3'

  if(High(av) > 2) then winfo.Speed:=av[3].VInt;
  if(High(av) > 3) then winfo.AverageRadius:=av[4].VInt;
  if(High(av) > 4) then winfo.SecondaryDamageRadius:=av[5].VInt;
  if(High(av) > 5) then winfo.MiningFactor:=av[6].VFloat;
  if High(av) > 6 then winfo.AttackCount:=av[7].VInt;
end;

procedure SF_SetCustomMissileWeaponStats(av:array of TVarEC; code:TCodeEC);
var winfo:PWeaponInfo;
begin
  if(High(av) < 5) then raise Exception.Create('Error.Script SetCustomMissileWeaponStats');
  winfo:=PWeaponInfo(av[1].VDW);
  av[0].VDW:=Cardinal(winfo);

  winfo.MissileRadius:=av[2].VInt;
  winfo.MissileMaxSpeed:=av[3].VInt;
  winfo.MissileMinSpeed:=av[4].VInt;
  winfo.MissileChanceToBeHit:=av[5].VInt;
end;

procedure SF_SetCustomWeaponSE(av:array of TVarEC; code:TCodeEC);
var winfo:PWeaponInfo;
begin
  if(High(av) < 5) then raise Exception.Create('Error.Script SetCustomWeaponSE');
  winfo:=PWeaponInfo(av[1].VDW);
  av[0].VDW:=Cardinal(winfo);

  winfo.PrimarySE:=av[2].VStr;//used by direct fire weapons (except area damage weapons) 'Weapon.0' - laser
  winfo.SecondarySE:=av[3].VStr;//can used by splash weapons (resonator 'Weapon.Nine') and area damage weapons (IMHO, uses same SE as primary), set to 'Weapon.NoGraph' if not needed
  winfo.AreaSE:=av[4].VStr;//used by missiles ('Weapon.MissileHit') and vertix (same name as primary), can be used by exploder, set to '' if not needed
  winfo.DefaultPalette:=av[5].VInt;//default shot visual (0 for normal weapons without modifications)
end;



procedure SF_StarCustomFaction(av:array of TVarEC; code:TCodeEC);
var star:TStar;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script StarCustomFaction');
  star:=TStar(av[1].VDW);
  av[0].VStr:=star.FStatus.CustomFaction;
  if High(av) > 1 then
  begin
    star.FStatus.CustomFaction:=av[2].VStr;
    if av[2].VStr='' then star.ResetStarOwner;//when clearing custom faction system will go to a side with most ships present
  end;
end;

//main.dat
//emblem in Data.Race.Emblem.2_faction_name

//Lang.dat
//planet text in Planet.faction_name.Info
//system controlled text in FormInfo.StarInfo.ControlledBy_faction_name
//military operation news in GalaxyNews.Group.WarriorLiberator.Create_faction_name

procedure SF_ShipCustomFaction(av:array of TVarEC; code:TCodeEC);
var ship:TShip;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script ShipCustomFaction');
  ship:=TShip(av[1].VDW);

  if ship=Player then
  begin
    if High(av) > 1 then raise Exception.Create('Error.Script ShipCustomFaction Player');
    av[0].VStr:='';
    exit;
  end;

  if ship.FScriptShip=nil then 
  begin
    if High(av) > 1 then raise Exception.Create('Error.Script ShipCustomFaction non-script ship');
    av[0].VStr:='';
    exit;
  end;

  av[0].VStr:=TScriptShip(ship.FScriptShip).FCustomFaction;
  if High(av) > 1 then
  begin
    TScriptShip(ship.FScriptShip).FCustomFaction:=av[2].VStr;
    ship.CalcStanding;
  end;
end;

//portraits in cachedata, (optional, standart rules will be used if not provided)
//Bm.Captain.

procedure SF_EqCustomFaction(av:array of TVarEC; code:TCodeEC);
var eq:TEquipment;
begin
  if High(av) < 1 then raise Exception.Create('Error.Script EqCustomFaction');
  eq:=TEquipment(av[1].VDW);
  av[0].VStr:=eq.FCustomFaction;
  if High(av) > 1 then eq.FCustomFaction:=av[2].VStr;
end;
//main.dat
//Data.SE.Items.faction_name0/1/2 for container



procedure SF_ImportedFunction(av:array of TVarEC; code:TCodeEC);
begin
  if High(av) < 2 then raise Exception.Create('Error.Script ImportedFunction');

  av[0].ChangeVType(vtLibraryFun);
  av[0].VStr:=av[1].VStr+','+av[2].VStr;

  if EC_DLL_Cache=nil then EC_DLL_Cache:=TLibraryCache.Create;
  EC_DLL_Cache.InitFunction(av[0]);
end;

procedure SF_ImportAll(av:array of TVarEC; code:TCodeEC);
begin
  if High(av) < 1 then raise Exception.Create('Error.Script ImportAll');

  if EC_DLL_Cache=nil then EC_DLL_Cache:=TLibraryCache.Create;
  EC_DLL_Cache.GetLib(av[1].VStr).InitAllFunctions( code.LocalVar );

  code.LinkAll(code.LocalVar);
end;

procedure SF_GalaxyPtr(av:array of TVarEC; code:TCodeEC);
begin
  av[0].VDW:=Cardinal(Galaxy);
end;


procedure ScriptFunInit(va:TVarArrayEC);
var i:integer;
    act:TActionType;
begin
  va.AddStdFunction;

  va.Add('GRun',vtExternFun).VExternFun:=SF_GRun;
  va.Add('GCntRun',vtExternFun).VExternFun:=SF_GCntRun;
  va.Add('GLastTurnRun',vtExternFun).VExternFun:=SF_GLastTurnRun;
  va.Add('GAllCntRun',vtExternFun).VExternFun:=SF_GAllCntRun;
  va.Add('IsScriptActive',vtExternFun).VExternFun:=SF_IsScriptActive;
  va.Add('GetValueFromScript',vtExternFun).VExternFun:=SF_GetValueFromScript;
  va.Add('GetVariableName',vtExternFun).VExternFun:=SF_GetVariableName;
  va.Add('GetVariableType',vtExternFun).VExternFun:=SF_GetVariableType;


  va.Add('StatusPlayer',vtExternFun).VExternFun:=SF_StatusPlayer;

  va.Add('AddPlanetNews',vtExternFun).VExternFun:=SF_AddPlanetNews;
  va.Add('AutoBattle',vtExternFun).VExternFun:=SF_AutoBattle;

  va.Add('GetOwner',vtExternFun).VExternFun:=SF_GetOwner;
  va.Add('GiveReward',vtExternFun).VExternFun:=SF_GiveReward;
  va.Add('GiveRewardByNom',vtExternFun).VExternFun:=SF_GiveRewardByNom;
  va.Add('CountReward',vtExternFun).VExternFun:=SF_CountReward;
  va.Add('CountRewardByNom',vtExternFun).VExternFun:=SF_CountRewardByNom;
  va.Add('DeleteRewardByNom',vtExternFun).VExternFun:=SF_DeleteRewardByNom;
  va.Add('Rnd',vtExternFun).VExternFun:=SF_Rnd;
  va.Add('GameDateTxtByTurn',vtExternFun).VExternFun:=SF_GameDateTxtByTurn;
  va.Add('Id',vtExternFun).VExternFun:=SF_Id;
  va.Add('SetName',vtExternFun).VExternFun:=SF_SetName;
  va.Add('UseTranclucator',vtExternFun).VExternFun:=SF_UseTranclucator;
  va.Add('HullDamage',vtExternFun).VExternFun:=SF_HullDamage;
  va.Add('Hitpoints',vtExternFun).VExternFun:=SF_Hitpoints;
  va.Add('Hit',vtExternFun).VExternFun:=SF_Hit;
  va.Add('ChangeGlobalRelationsShips',vtExternFun).VExternFun:=SF_ChangeGlobalRelationsShips;
  va.Add('ChangeGlobalRelationsPlanets',vtExternFun).VExternFun:=SF_ChangeGlobalRelationsPlanets;
  va.Add('GlobalRelationsShips',vtExternFun).VExternFun:=SF_GlobalRelationsShips;
  va.Add('GlobalRelationsPlanets',vtExternFun).VExternFun:=SF_GlobalRelationsPlanets;
  va.Add('SetRelationGroup',vtExternFun).VExternFun:=SF_SetRelationGroup;
  va.Add('SetRelationPlanet',vtExternFun).VExternFun:=SF_SetRelationPlanet;
  va.Add('GetRelationPlanet',vtExternFun).VExternFun:=SF_GetRelationPlanet;
  va.Add('CurTurn',vtExternFun).VExternFun:=SF_CurTurn;
  va.Add('ShipType',vtExternFun).VExternFun:=SF_ShipType;
  va.Add('ConName',vtExternFun).VExternFun:=SF_ConName;
  va.Add('StarName',vtExternFun).VExternFun:=SF_StarName;
  va.Add('StarMapLabel',vtExternFun).VExternFun:=SF_StarMapLabel;
  va.Add('PlanetName',vtExternFun).VExternFun:=SF_PlanetName;
  va.Add('IdToPlanet',vtExternFun).VExternFun:=SF_IdToPlanet;
  va.Add('IdToShip',vtExternFun).VExternFun:=SF_IdToShip;
  va.Add('IdToItem',vtExternFun).VExternFun:=SF_IdToItem;
  va.Add('PlanetSetGoods',vtExternFun).VExternFun:=SF_PlanetSetGoods;
  va.Add('ShipName',vtExternFun).VExternFun:=SF_ShipName;
  va.Add('ShipRank',vtExternFun).VExternFun:=SF_ShipRank;
  va.Add('ShipRankPoints',vtExternFun).VExternFun:=SF_ShipRankPoints;
  va.Add('ShipNextRankPoints',vtExternFun).VExternFun:=SF_ShipNextRankPoints;
  va.Add('ShipRaiseRank',vtExternFun).VExternFun:=SF_ShipRaiseRank;
  va.Add('ShipStar',vtExternFun).VExternFun:=SF_ShipStar;
  va.Add('StarToCon',vtExternFun).VExternFun:=SF_StarToCon;
  va.Add('ConNear',vtExternFun).VExternFun:=SF_ConNear;
  va.Add('ConStars',vtExternFun).VExternFun:=SF_ConStars;
  va.Add('ConStar',vtExternFun).VExternFun:=SF_ConStar;
  va.Add('GalaxyStars',vtExternFun).VExternFun:=SF_GalaxyStars;
  va.Add('GalaxyStar',vtExternFun).VExternFun:=SF_GalaxyStar;
  va.Add('StarAngleBetween',vtExternFun).VExternFun:=SF_StarAngleBetween;
  va.Add('FindPlanet',vtExternFun).VExternFun:=SF_FindPlanet;
  va.Add('IsPlayer',vtExternFun).VExternFun:=SF_IsPlayer;
  va.Add('GroupCount',vtExternFun).VExternFun:=SF_GroupCount;
  va.Add('GroupIn',vtExternFun).VExternFun:=SF_GroupIn;
  va.Add('CountIn',vtExternFun).VExternFun:=SF_CountIn;
  va.Add('ChangeState',vtExternFun).VExternFun:=SF_ChangeState;
  va.Add('NearestGroup',vtExternFun).VExternFun:=SF_NearestGroup;
  va.Add('StarAngle',vtExternFun).VExternFun:=SF_StarAngle;
  va.Add('NewsAdd',vtExternFun).VExternFun:=SF_NewsAdd;
  va.Add('MsgAdd',vtExternFun).VExternFun:=SF_MsgAdd;
  va.Add('Ether',vtExternFun).VExternFun:=SF_Ether;
  va.Add('CustomEther',vtExternFun).VExternFun:=SF_CustomEther;
  va.Add('EtherDelete',vtExternFun).VExternFun:=SF_EtherDelete;
  va.Add('EtherIdAdd',vtExternFun).VExternFun:=SF_EtherIdAdd;
  va.Add('EtherIdDelete',vtExternFun).VExternFun:=SF_EtherIdDelete;
  va.Add('EtherState',vtExternFun).VExternFun:=SF_EtherState;
  va.Add('ConChangeRelationToRanger',vtExternFun).VExternFun:=SF_ConChangeRelationToRanger;
  va.Add('GetData',vtExternFun).VExternFun:=SF_GetData;
  va.Add('SetData',vtExternFun).VExternFun:=SF_SetData;
  va.Add('ShipData',vtExternFun).VExternFun:=SF_ShipData;
  va.Add('Format',vtExternFun).VExternFun:=SF_Format;
  va.Add('DeleteTags',vtExternFun).VExternFun:=SF_DeleteTags;
  va.Add('Dialog',vtExternFun).VExternFun:=SF_Dialog;
  va.Add('DText',vtExternFun).VExternFun:=SF_DText;
  va.Add('DAddText',vtExternFun).VExternFun:=SF_DAddText;
  va.Add('DAdd',vtExternFun).VExternFun:=SF_DAdd;
  va.Add('DChange',vtExternFun).VExternFun:=SF_DChange;
  va.Add('DAnswer',vtExternFun).VExternFun:=SF_DAnswer;
  va.Add('Player',vtExternFun).VExternFun:=SF_Player;
  va.Add('ItemExist',vtExternFun).VExternFun:=SF_ItemExist;
  va.Add('ItemIn',vtExternFun).VExternFun:=SF_ItemIn;
  va.Add('ItemCost',vtExternFun).VExternFun:=SF_ItemCost;
  va.Add('ItemCount',vtExternFun).VExternFun:=SF_ItemCount;
  va.Add('ShipPicksItem',vtExternFun).VExternFun:=SF_ShipPicksItem;
  va.Add('DropItem',vtExternFun).VExternFun:=SF_DropItem;
  va.Add('DropScriptItem',vtExternFun).VExternFun:=SF_DropScriptItem;
  va.Add('DeleteEquipment',vtExternFun).VExternFun:=SF_DeleteEquipment;
  va.Add('DecayGoods',vtExternFun).VExternFun:=SF_DecayGoods;
  va.Add('UpsurgeGoods',vtExternFun).VExternFun:=SF_UpsurgeGoods;
  va.Add('GoodsAdd',vtExternFun).VExternFun:=SF_GoodsAdd;
  va.Add('GoodsCount',vtExternFun).VExternFun:=SF_GoodsCount;
  va.Add('GoodsCost',vtExternFun).VExternFun:=SF_GoodsCost;
  va.Add('GoodsRuinsForBuy',vtExternFun).VExternFun:=SF_GoodsRuinsForBuy;
  va.Add('ShipGoods',vtExternFun).VExternFun:=SF_ShipGoods;
  va.Add('ShipGoodsIllegalOnPlanet',vtExternFun).VExternFun:=SF_ShipGoodsIllegalOnPlanet;
  va.Add('GoodsDrop',vtExternFun).VExternFun:=SF_GoodsDrop;
  va.Add('UselessItemCreate',vtExternFun).VExternFun:=SF_UselessItemCreate;
  va.Add('GoodsSellPrice',vtExternFun).VExternFun:=SF_GoodsSellPrice;
  va.Add('GoodsBuyPrice',vtExternFun).VExternFun:=SF_GoodsBuyPrice;
  va.Add('CountTurn',vtExternFun).VExternFun:=SF_CountTurn;
  va.Add('ShipSetBad',vtExternFun).VExternFun:=SF_ShipSetBad;
  va.Add('GroupSetBad',vtExternFun).VExternFun:=SF_GroupSetBad;
  va.Add('ShipSetPartner',vtExternFun).VExternFun:=SF_ShipSetPartner;
  va.Add('ShipJoin',vtExternFun).VExternFun:=SF_ShipJoin;
  va.Add('ShipOut',vtExternFun).VExternFun:=SF_ShipOut;
  va.Add('AllShipOut',vtExternFun).VExternFun:=SF_AllShipOut;
  va.Add('ShipInScript',vtExternFun).VExternFun:=SF_ShipInScript;
  va.Add('ShipInGameEvent',vtExternFun).VExternFun:=SF_ShipInGameEvent;
  va.Add('ShipInCurScript',vtExternFun).VExternFun:=SF_ShipInCurScript;
  va.Add('ShipInNormalSpace',vtExternFun).VExternFun:=SF_ShipInNormalSpace;
  va.Add('ShipInHole',vtExternFun).VExternFun:=SF_ShipInHole;
  va.Add('ShipIsTakeoff',vtExternFun).VExternFun:=SF_ShipIsTakeoff;

  va.Add('ShipCntWeapon',vtExternFun).VExternFun:=SF_ShipCntWeapon;
  va.Add('ShipWeapon',vtExternFun).VExternFun:=SF_ShipWeapon;
  va.Add('ShipEqInSlot',vtExternFun).VExternFun:=SF_ShipEqInSlot;
  va.Add('ArtefactTypeInUse',vtExternFun).VExternFun:=SF_ArtefactTypeInUse;
  va.Add('ArtefactTypeBoosted',vtExternFun).VExternFun:=SF_ArtefactTypeBoosted;
  va.Add('ShipSpeed',vtExternFun).VExternFun:=SF_ShipSpeed;
  va.Add('EnginePower',vtExternFun).VExternFun:=SF_EnginePower;
  va.Add('ShipJump',vtExternFun).VExternFun:=SF_ShipJump;
  va.Add('ShipArmor',vtExternFun).VExternFun:=SF_ShipArmor;
  va.Add('ShipProtectability',vtExternFun).VExternFun:=SF_ShipProtectability;
  va.Add('ShipDroidRepair',vtExternFun).VExternFun:=SF_ShipDroidRepair;
  va.Add('ShipRadarRange',vtExternFun).VExternFun:=SF_ShipRadarRange;
  va.Add('ShipScanerPower',vtExternFun).VExternFun:=SF_ShipScanerPower;
  va.Add('ShipHookPower',vtExternFun).VExternFun:=SF_ShipHookPower;
  va.Add('ShipHookRange',vtExternFun).VExternFun:=SF_ShipHookRange;
  va.Add('ShipAverageDamage',vtExternFun).VExternFun:=SF_ShipAverageDamage;

  va.Add('ShipHealthFactor',vtExternFun).VExternFun:=SF_ShipHealthFactor;
  va.Add('ShipHealthFactorStatus',vtExternFun).VExternFun:=SF_ShipHealthFactorStatus;
  va.Add('PlayerImmunity',vtExternFun).VExternFun:=SF_PlayerImmunity;

  va.Add('ShipStatusEffect',vtExternFun).VExternFun:=SF_ShipStatusEffect;

  va.Add('ShipGroup',vtExternFun).VExternFun:=SF_ShipGroup;
  va.Add('ShipCanJump',vtExternFun).VExternFun:=SF_ShipCanJump;
  va.Add('ShipInStar',vtExternFun).VExternFun:=SF_ShipInStar;
  va.Add('ShipInPlanet',vtExternFun).VExternFun:=SF_ShipInPlanet;
  va.Add('ShipStatistic',vtExternFun).VExternFun:=SF_ShipStatistic;
  va.Add('PlayerDominatorStatistic',vtExternFun).VExternFun:=SF_PlayerDominatorStatistic;
  va.Add('ShipMoney',vtExternFun).VExternFun:=SF_ShipMoney;
  va.Add('ShipFuel',vtExternFun).VExternFun:=SF_ShipFuel;
  va.Add('ShipFuelLow',vtExternFun).VExternFun:=SF_ShipFuelLow;
  va.Add('ShipStrengthInBestRanger',vtExternFun).VExternFun:=SF_ShipStrengthInBestRanger;
  va.Add('ShipStrengthInAverageRanger',vtExternFun).VExternFun:=SF_ShipStrengthInAverageRanger;
  va.Add('ChanceToWin',vtExternFun).VExternFun:=SF_ChanceToWin;

  va.Add('ShipFind',vtExternFun).VExternFun:=SF_ShipFind;
  va.Add('RangerStatus',vtExternFun).VExternFun:=SF_RangerStatus;
  va.Add('RangerPlaceInRating',vtExternFun).VExternFun:=SF_RangerPlaceInRating;
  va.Add('RangerExcludedFromRating',vtExternFun).VExternFun:=SF_RangerExcludedFromRating;
  va.Add('GalaxyMoney',vtExternFun).VExternFun:=SF_GalaxyMoney;
  va.Add('ShipDestroy',vtExternFun).VExternFun:=SF_ShipDestroy;
  va.Add('ShipDestroyType',vtExternFun).VExternFun:=SF_ShipDestroyType;
  va.Add('ItemDestroy',vtExternFun).VExternFun:=SF_ItemDestroy;
  va.Add('RangersCapital',vtExternFun).VExternFun:=SF_RangersCapital;
  va.Add('GroupToShip',vtExternFun).VExternFun:=SF_GroupToShip;
  va.Add('OrderLanding',vtExternFun).VExternFun:=SF_OrderLanding;
  va.Add('OrderJump',vtExternFun).VExternFun:=SF_OrderJump;
  va.Add('GroupIs',vtExternFun).VExternFun:=SF_GroupIs;
  va.Add('StateIs',vtExternFun).VExternFun:=SF_StateIs;
  va.Add('Dist',vtExternFun).VExternFun:=SF_Dist;
  va.Add('Angle',vtExternFun).VExternFun:=SF_Angle;
  va.Add('Dist2Star',vtExternFun).VExternFun:=SF_Dist2Star;
  va.Add('BuyPirate',vtExternFun).VExternFun:=SF_BuyPirate;
  va.Add('BuyTransport',vtExternFun).VExternFun:=SF_BuyTransport;
  va.Add('Name',vtExternFun).VExternFun:=SF_Name;
  va.Add('ShortName',vtExternFun).VExternFun:=SF_ShortName;

  va.Add('FirstGiveMoney',vtExternFun).VExternFun:=SF_FirstGiveMoney;
  //va.Add('ScenarioState',vtExternFun).VExternFun:=SF_ScenarioState;
  //va.Add('HaveCommunicator',vtExternFun).VExternFun:=SF_HaveCommunicator;
  va.Add('HaveProgramm',vtExternFun).VExternFun:=SF_HaveProgramm;
  va.Add('GetProgramm',vtExternFun).VExternFun:=SF_GetProgramm;
  va.Add('SetProgramm',vtExternFun).VExternFun:=SF_SetProgramm;
  va.Add('DomikProgramm',vtExternFun).VExternFun:=SF_DomikProgramm;
  va.Add('DomikProgrammDate',vtExternFun).VExternFun:=SF_DomikProgrammDate;
  va.Add('HoleMamaCreate',vtExternFun).VExternFun:=SF_HoleMamaCreate;
  va.Add('HoleCreate',vtExternFun).VExternFun:=SF_HoleCreate;

  va.Add('TerronWeaponLock',vtExternFun).VExternFun:=SF_TerronWeaponLock;
  va.Add('TerronGrowLock',vtExternFun).VExternFun:=SF_TerronGrowLock;
  va.Add('TerronLandingLock',vtExternFun).VExternFun:=SF_TerronLandingLock;
  va.Add('TerronToStar',vtExternFun).VExternFun:=SF_TerronToStar;
  va.Add('KellerLeave',vtExternFun).VExternFun:=SF_KellerLeave;
  va.Add('KellerNewResearch',vtExternFun).VExternFun:=SF_KellerNewResearch;
  va.Add('KellerKill',vtExternFun).VExternFun:=SF_KellerKill;
  va.Add('BlazerLanding',vtExternFun).VExternFun:=SF_BlazerLanding;
  va.Add('BlazerSelfDestruction',vtExternFun).VExternFun:=SF_BlazerSelfDestruction;

  va.Add('GalaxyShipId',vtExternFun).VExternFun:=SF_GalaxyShipId;

  va.Add('NearCivilPlanet',vtExternFun).VExternFun:=SF_NearCivilPlanet;

  va.Add('SkipGreeting',vtExternFun).VExternFun:=SF_SkipGreeting;
  va.Add('Sound',vtExternFun).VExternFun:=SF_Sound;

  va.Add('Tips',vtExternFun).VExternFun:=SF_Tips;
  va.Add('TipsState',vtExternFun).VExternFun:=SF_TipsState;
  va.Add('CT',vtExternFun).VExternFun:=SF_CT;
  va.Add('BlockExist',vtExternFun).VExternFun:=SF_BlockExist;
  va.Add('GetMainData',vtExternFun).VExternFun:=SF_GetMainData;
  va.Add('GetGameOptions',vtExternFun).VExternFun:=SF_GetGameOptions;
  va.Add('ResourceExist',vtExternFun).VExternFun:=SF_ResourceExist;
  va.Add('SFT',vtExternFun).VExternFun:=SF_SFT;

  va.Add('CurrentMods',vtExternFun).VExternFun:=SF_CurrentMods;
  va.Add('RobotSupport',vtExternFun).VExternFun:=SF_RobotSupport;

  va.Add('UselessItem',vtInt).VInt:=integer(t_UselessItem);

  va.Add('ForLiberationSystem',vtInt).VInt:=integer(ForLiberationSystem);
  va.Add('ForAccomplishment',vtInt).VInt:=integer(ForAccomplishment);
  va.Add('ForSecretMission',vtInt).VInt:=integer(ForSecretMission);
  va.Add('ForCowardice',vtInt).VInt:=integer(ForCowardice);
  va.Add('ForPerfidy',vtInt).VInt:=integer(ForPerfidy);
  va.Add('ForPlanetBattle',vtInt).VInt:=integer(ForPlanetBattle);

  va.Add('Maloc',vtInt).VInt:=integer(Maloc);
  va.Add('Peleng',vtInt).VInt:=integer(Peleng);
  va.Add('People',vtInt).VInt:=integer(People);
  va.Add('Fei',vtInt).VInt:=integer(Fei);
  va.Add('Gaal',vtInt).VInt:=integer(Gaal);
  va.Add('Kling',vtInt).VInt:=integer(Kling);
  va.Add('None',vtInt).VInt:=integer(None);
  va.Add('PirateClan',vtInt).VInt:=integer(PirateClan);

  va.Add('t_Food',vtInt).VInt:=integer(t_Food);
  va.Add('t_Medicine',vtInt).VInt:=integer(t_Medicine);
  va.Add('t_Technics',vtInt).VInt:=integer(t_Technics);
  va.Add('t_Luxury',vtInt).VInt:=integer(t_Luxury);
  va.Add('t_Minerals',vtInt).VInt:=integer(t_Minerals);
  va.Add('t_Alcohol',vtInt).VInt:=integer(t_Alcohol);
  va.Add('t_Arms',vtInt).VInt:=integer(t_Arms);
  va.Add('t_Narcotics',vtInt).VInt:=integer(t_Narcotics);

  va.Add('t_Artefact',vtInt).VInt:=integer(t_Artefact);//custom arts
  va.Add('t_Artefact2',vtInt).VInt:=integer(t_Artefact2);//custom arts

  va.Add('t_ArtefactHull',vtInt).VInt:=integer(t_ArtefactHull);
  va.Add('t_ArtefactFuel',vtInt).VInt:=integer(t_ArtefactFuel);
  va.Add('t_ArtefactSpeed',vtInt).VInt:=integer(t_ArtefactSpeed);
  va.Add('t_ArtefactPower',vtInt).VInt:=integer(t_ArtefactPower);
  va.Add('t_ArtefactRadar',vtInt).VInt:=integer(t_ArtefactRadar);
  va.Add('t_ArtefactScaner',vtInt).VInt:=integer(t_ArtefactScaner);
  va.Add('t_ArtefactDroid',vtInt).VInt:=integer(t_ArtefactDroid);
  va.Add('t_ArtefactNano',vtInt).VInt:=integer(t_ArtefactNano);
  va.Add('t_ArtefactHook',vtInt).VInt:=integer(t_ArtefactHook);
  va.Add('t_ArtefactDef',vtInt).VInt:=integer(t_ArtefactDef);
  va.Add('t_ArtefactAnalyzer',vtInt).VInt:=integer(t_ArtefactAnalyzer);
  va.Add('t_ArtefactMiniExpl',vtInt).VInt:=integer(t_ArtefactMiniExpl);
  va.Add('t_ArtefactAntigrav',vtInt).VInt:=integer(t_ArtefactAntigrav);
  va.Add('t_ArtefactTransmitter',vtInt).VInt:=integer(t_ArtefactTransmitter);
  va.Add('t_ArtefactBomb',vtInt).VInt:=integer(t_ArtefactBomb);
  va.Add('t_ArtefactTranclucator',vtInt).VInt:=integer(t_ArtefactTranclucator);
  va.Add('t_Hull',vtInt).VInt:=integer(t_Hull);
  va.Add('t_FuelTanks',vtInt).VInt:=integer(t_FuelTanks);
  va.Add('t_Engine',vtInt).VInt:=integer(t_Engine);
  va.Add('t_Radar',vtInt).VInt:=integer(t_Radar);
  va.Add('t_Scaner',vtInt).VInt:=integer(t_Scaner);
  va.Add('t_RepairRobot',vtInt).VInt:=integer(t_RepairRobot);
  va.Add('t_CargoHook',vtInt).VInt:=integer(t_CargoHook);
  va.Add('t_DefGenerator',vtInt).VInt:=integer(t_DefGenerator);

  for i:=1 to ItemSetCount(HardCodedWeapons) do va.Add('t_Weapon'+inttostr(i),vtInt).VInt:=integer(ItemSetMember(HardCodedWeapons,i));
  va.Add('t_CustomWeapon',vtInt).VInt:=integer(t_CustomWeapon);

  va.Add('t_Protoplasm',vtInt).VInt:=integer(t_Protoplasm);
  va.Add('t_UselessItem',vtInt).VInt:=integer(t_UselessItem);

  va.Add('ReWar',vtInt).VInt:=integer(ReWar);
  va.Add('ReBad',vtInt).VInt:=integer(ReBad);
  va.Add('ReNormal',vtInt).VInt:=integer(ReNormal);
  va.Add('ReGood',vtInt).VInt:=integer(ReGood);
  va.Add('ReBest',vtInt).VInt:=integer(ReBest);

  va.Add('Trader',vtInt).VInt:=integer(Trader);
  va.Add('Pirate',vtInt).VInt:=integer(Pirate);
  va.Add('Warrior',vtInt).VInt:=integer(Warrior);

  va.Add('t_Kling',vtInt).VInt:=integer(t_Kling);
  va.Add('t_Ranger',vtInt).VInt:=integer(t_Ranger);
  va.Add('t_Transport',vtInt).VInt:=integer(t_Transport);
  va.Add('t_Pirate',vtInt).VInt:=integer(t_Pirate);
  va.Add('t_Warrior',vtInt).VInt:=integer(t_Warrior);
  va.Add('t_Tranclucator',vtInt).VInt:=integer(t_Tranclucator);
  va.Add('t_RC',vtInt).VInt:=integer(t_RC);
  va.Add('t_PB',vtInt).VInt:=integer(t_PB);
  va.Add('t_WB',vtInt).VInt:=integer(t_WB);
  va.Add('t_SB',vtInt).VInt:=integer(t_SB);
  va.Add('t_BK',vtInt).VInt:=integer(t_BK);
  va.Add('t_MC',vtInt).VInt:=integer(t_MC);
  va.Add('t_CB',vtInt).VInt:=integer(t_CB);
  va.Add('t_UB',vtInt).VInt:=integer(t_UB);

  va.Add('progKellerCall',vtInt).VInt:=integer(progKellerCall);
  va.Add('progLogicalNegation',vtInt).VInt:=integer(progLogicalNegation);
  va.Add('progDematerial',vtInt).VInt:=integer(progDematerial);
  va.Add('progEnergotron',vtInt).VInt:=integer(progEnergotron);
  va.Add('progSabCrack',vtInt).VInt:=integer(progSabCrack);
  va.Add('progIntercom',vtInt).VInt:=integer(progIntercom);

  va.Add('StarShips',vtExternFun).VExternFun:=SF_StarShips;
  va.Add('StarPlanets',vtExternFun).VExternFun:=SF_StarPlanets;
  va.Add('StarMissiles',vtExternFun).VExternFun:=SF_StarMissiles;
  va.Add('StarAsteroids',vtExternFun).VExternFun:=SF_StarAsteroids;

  va.Add('GroupShip',vtExternFun).VExternFun:=SF_GroupShip;
  va.Add('ShipItems',vtExternFun).VExternFun:=SF_ShipItems;
  va.Add('ShipArts',vtExternFun).VExternFun:=SF_ShipArts;
  va.Add('PlayerTranclucators',vtExternFun).VExternFun:=SF_PlayerTranclucators;
  va.Add('ArtTranclucatorToShip',vtExternFun).VExternFun:=SF_ArtTranclucatorToShip;
  va.Add('TranclucatorData',vtExternFun).VExternFun:=SF_TranclucatorData;
  va.Add('LinkItemToScript',vtExternFun).VExternFun:=SF_LinkItemToScript;
  va.Add('ReleaseItemFromScript',vtExternFun).VExternFun:=SF_ReleaseItemFromScript;
  va.Add('ScriptItemData',vtExternFun).VExternFun:=SF_ScriptItemData;
  va.Add('ScriptItemTextData',vtExternFun).VExternFun:=SF_ScriptItemTextData;
  va.Add('ScriptItemToItem',vtExternFun).VExternFun:=SF_ScriptItemToItem;

  va.Add('GetShipPirateRank',vtExternFun).VExternFun:=SF_GetShipPirateRank;
  va.Add('ShipPirateRankPoints',vtExternFun).VExternFun:=SF_ShipPirateRankPoints;
  va.Add('ShipNextPirateRankPoints',vtExternFun).VExternFun:=SF_ShipNextPirateRankPoints;
  va.Add('ShipInPirateClan',vtExternFun).VExternFun:=SF_ShipInPirateClan;
  va.Add('ShipOnSidePirateClan',vtExternFun).VExternFun:=SF_ShipOnSidePirateClan;
  va.Add('RaisePirateRank',vtExternFun).VExternFun:=SF_RaisePirateRank;

  va.Add('ItemType',vtExternFun).VExternFun:=SF_ItemType;
  va.Add('CustomWeaponType',vtExternFun).VExternFun:=SF_CustomWeaponType;
  va.Add('ItemName',vtExternFun).VExternFun:=SF_ItemName;
  va.Add('ItemFullName',vtExternFun).VExternFun:=SF_ItemFullName;
  va.Add('ItemSize',vtExternFun).VExternFun:=SF_ItemSize;
  va.Add('ItemOwner',vtExternFun).VExternFun:=SF_ItemOwner;
  va.Add('ItemSubrace',vtExternFun).VExternFun:=SF_ItemSubrace;
  va.Add('ItemIsInUse',vtExternFun).VExternFun:=SF_ItemIsInUse;
  va.Add('ItemIsInSet',vtExternFun).VExternFun:=SF_ItemIsInSet;
  va.Add('PlayerEqSet',vtExternFun).VExternFun:=SF_PlayerEqSet;
  va.Add('ItemIsBroken',vtExternFun).VExternFun:=SF_ItemIsBroken;

  va.Add('ShipCanUseEq',vtExternFun).VExternFun:=SF_ShipCanUseEq;
  va.Add('ShipCanRepairEq',vtExternFun).VExternFun:=SF_ShipCanRepairEq;
  va.Add('ShipTechLevelKnowledge',vtExternFun).VExternFun:=SF_ShipTechLevelKnowledge;

  va.Add('WeaponTarget',vtExternFun).VExternFun:=SF_WeaponTarget;
  va.Add('GetEquipmentStats',vtExternFun).VExternFun:=SF_GetEquipmentStats;
  va.Add('SetEquipmentStats',vtExternFun).VExternFun:=SF_SetEquipmentStats;
  va.Add('CreateHull',vtExternFun).VExternFun:=SF_CreateHull;
  va.Add('CreateEquipment',vtExternFun).VExternFun:=SF_CreateEquipment;
  va.Add('CreateArt',vtExternFun).VExternFun:=SF_CreateArt;
  va.Add('CreateCustomWeapon',vtExternFun).VExternFun:=SF_CreateCustomWeapon;
  va.Add('CreateCustomArt',vtExternFun).VExternFun:=SF_CreateCustomArt;
  va.Add('CustomArtData',vtExternFun).VExternFun:=SF_CustomArtData;
  va.Add('CustomArtTextData',vtExternFun).VExternFun:=SF_CustomArtTextData;
  va.Add('CreateMM',vtExternFun).VExternFun:=SF_CreateMM;
  va.Add('CreateNodes',vtExternFun).VExternFun:=SF_CreateNodes;
  va.Add('CreateCustomCountableItem',vtExternFun).VExternFun:=SF_CreateCustomCountableItem;
  va.Add('CreateZond',vtExternFun).VExternFun:=SF_CreateZond;
  va.Add('ExistingZonds',vtExternFun).VExternFun:=SF_ExistingZonds;
  va.Add('FreeItem',vtExternFun).VExternFun:=SF_FreeItem;

  va.Add('ShipJoinsClan',vtExternFun).VExternFun:=SF_ShipJoinsClan;

  va.Add('AddItemToShip',vtExternFun).VExternFun:=SF_AddItemToShip;
  va.Add('GetItemFromShip',vtExternFun).VExternFun:=SF_GetItemFromShip;
  va.Add('GetArtFromShip',vtExternFun).VExternFun:=SF_GetArtFromShip;
  va.Add('ArrangeItems',vtExternFun).VExternFun:=SF_ArrangeItems;
  va.Add('AddItemToPlanet',vtExternFun).VExternFun:=SF_AddItemToPlanet;
  va.Add('GetItemFromPlanet',vtExternFun).VExternFun:=SF_GetItemFromPlanet;
  va.Add('AddItemToShop',vtExternFun).VExternFun:=SF_AddItemToShop;
  va.Add('GetItemFromShop',vtExternFun).VExternFun:=SF_GetItemFromShop;
  va.Add('AddItemToStorage',vtExternFun).VExternFun:=SF_AddItemToStorage;
  va.Add('GetItemFromStorage',vtExternFun).VExternFun:=SF_GetItemFromStorage;
  va.Add('FindItemInStorage',vtExternFun).VExternFun:=SF_FindItemInStorage;
  va.Add('PutItemInVault',vtExternFun).VExternFun:=SF_PutItemInVault;
  va.Add('GetItemFromVault',vtExternFun).VExternFun:=SF_GetItemFromVault;
  va.Add('DropItemInSystem',vtExternFun).VExternFun:=SF_DropItemInSystem;
  va.Add('StopMovingItem',vtExternFun).VExternFun:=SF_StopMovingItem;

  va.Add('StarItems',vtExternFun).VExternFun:=SF_StarItems;
  va.Add('GetItemFromStar',vtExternFun).VExternFun:=SF_GetItemFromStar;
  va.Add('PlanetItems',vtExternFun).VExternFun:=SF_PlanetItems;

  va.Add('StorageItems',vtExternFun).VExternFun:=SF_StorageItems;
  va.Add('StorageItemLocation',vtExternFun).VExternFun:=SF_StorageItemLocation;

  va.Add('ShopItems',vtExternFun).VExternFun:=SF_ShopItems;

  va.Add('AddDialogOverride',vtExternFun).VExternFun:=SF_AddDialogOverride;
  va.Add('AddDialogInject',vtExternFun).VExternFun:=SF_AddDialogInject;
  va.Add('InjectAnswer',vtExternFun).VExternFun:=SF_InjectAnswer;
  va.Add('AddDialogBlock',vtExternFun).VExternFun:=SF_AddDialogBlock;
  va.Add('GotoGov',vtExternFun).VExternFun:=SF_GotoGov;
  va.Add('GetShipPlanet',vtExternFun).VExternFun:=SF_GetShipPlanet;
  va.Add('GetShipHomePlanet',vtExternFun).VExternFun:=SF_GetShipHomePlanet;
  va.Add('GetShipRuins',vtExternFun).VExternFun:=SF_GetShipRuins;
  va.Add('GetTalkShip',vtExternFun).VExternFun:=SF_GetTalkShip;
  va.Add('GetTalkType',vtExternFun).VExternFun:=SF_GetTalkType;
  va.Add('TalkByAI',vtExternFun).VExternFun:=SF_TalkByAI;

  va.Add('ScriptRun',vtExternFun).VExternFun:=SF_ScriptRun;

  va.Add('CreateABShip',vtExternFun).VExternFun:=SF_CreateABShip;
  va.Add('ConvertToABShip',vtExternFun).VExternFun:=SF_ConvertToABShip;
  va.Add('ABShipModifiers',vtExternFun).VExternFun:=SF_ABShipModifiers;
  va.Add('StartAB',vtExternFun).VExternFun:=SF_StartAB;

  va.Add('StartTextQuest',vtExternFun).VExternFun:=SF_StartTextQuest;
  va.Add('StartRobots',vtExternFun).VExternFun:=SF_StartRobots;
  va.Add('MarkRobotsMapAsUsed',vtExternFun).VExternFun:=SF_MarkRobotsMapAsUsed;

  va.Add('ShipOwner',vtExternFun).VExternFun:=SF_ShipOwner;
  va.Add('ShipPilotRace',vtExternFun).VExternFun:=SF_ShipPilotRace;
  va.Add('ShipSkill',vtExternFun).VExternFun:=SF_ShipSkill;
  va.Add('ShipFace',vtExternFun).VExternFun:=SF_ShipFace;

  va.Add('ShipFreeExp',vtExternFun).VExternFun:=SF_ShipFreeExp;
  va.Add('GetShipExpByType',vtExternFun).VExternFun:=SF_GetShipExpByType;

  va.Add('CoordX',vtExternFun).VExternFun:=SF_CoordX;
  va.Add('CoordY',vtExternFun).VExternFun:=SF_CoordY;
  va.Add('ShipSetCoords',vtExternFun).VExternFun:=SF_ShipSetCoords;
  va.Add('ShipAngle',vtExternFun).VExternFun:=SF_ShipAngle;
  va.Add('ObjectType',vtExternFun).VExternFun:=SF_ObjectType;
  va.Add('ShipInHyperSpace',vtExternFun).VExternFun:=SF_ShipInHyperSpace;
  va.Add('ShipStatus',vtExternFun).VExternFun:=SF_ShipStatus;
  va.Add('BuyRanger',vtExternFun).VExternFun:=SF_BuyRanger;
  va.Add('BuyWarrior',vtExternFun).VExternFun:=SF_BuyWarrior;
  va.Add('BuyBigWarrior',vtExternFun).VExternFun:=SF_BuyBigWarrior;
  va.Add('BuyDomik',vtExternFun).VExternFun:=SF_BuyDomik;
  va.Add('BuyDomikExtremal',vtExternFun).VExternFun:=SF_BuyDomikExtremal;
  va.Add('BuyTranclucator',vtExternFun).VExternFun:=SF_BuyTranclucator;
  va.Add('TransferShip',vtExternFun).VExternFun:=SF_TransferShip;

  va.Add('OrderForsage',vtExternFun).VExternFun:=SF_OrderForsage;
  va.Add('OrderNone',vtExternFun).VExternFun:=SF_OrderNone;
  va.Add('OrderMove',vtExternFun).VExternFun:=SF_OrderMove;
  va.Add('OrderTeleport',vtExternFun).VExternFun:=SF_OrderTeleport;
  va.Add('OrderTakeOff',vtExternFun).VExternFun:=SF_OrderTakeOff;
  va.Add('OrderFollowShip',vtExternFun).VExternFun:=SF_OrderFollowShip;
  va.Add('OrderJumpHole',vtExternFun).VExternFun:=SF_OrderJumpHole;

  va.Add('RelationToRanger',vtExternFun).VExternFun:=SF_RelationToRanger;
  va.Add('RelationToShip',vtExternFun).VExternFun:=SF_RelationToShip;

  va.Add('StarOwner',vtExternFun).VExternFun:=SF_StarOwner;
  va.Add('StarBattle',vtExternFun).VExternFun:=SF_StarBattle;
  va.Add('StarSeries',vtExternFun).VExternFun:=SF_StarSeries;
  va.Add('StarHoles',vtExternFun).VExternFun:=SF_StarHoles;
  va.Add('StarNearbyStars',vtExternFun).VExternFun:=SF_StarNearbyStars;
  va.Add('StarNearbyStarsDist',vtExternFun).VExternFun:=SF_StarNearbyStarsDist;
  va.Add('StarSetGraph',vtExternFun).VExternFun:=SF_StarSetGraph;
  va.Add('CreatePlanet',vtExternFun).VExternFun:=SF_CreatePlanet;
  va.Add('PlanetSetGraph',vtExternFun).VExternFun:=SF_PlanetSetGraph;
  va.Add('PlanetGetGraph',vtExternFun).VExternFun:=SF_PlanetGetGraph;
  va.Add('PlanetPopulation',vtExternFun).VExternFun:=SF_PlanetPopulation;
  va.Add('PlanetOwner',vtExternFun).VExternFun:=SF_PlanetOwner;
  va.Add('PlanetRace',vtExternFun).VExternFun:=SF_PlanetRace;
  va.Add('PlanetGov',vtExternFun).VExternFun:=SF_PlanetGov;
  va.Add('PlanetEco',vtExternFun).VExternFun:=SF_PlanetEco;
  va.Add('PlanetTerrain',vtExternFun).VExternFun:=SF_PlanetTerrain;
  va.Add('PlanetTerrainExplored',vtExternFun).VExternFun:=SF_PlanetTerrainExplored;
  va.Add('PlanetOrbitRadius',vtExternFun).VExternFun:=SF_PlanetOrbitRadius;
  va.Add('PlanetOrbitalVelocity',vtExternFun).VExternFun:=SF_PlanetOrbitalVelocity;
  va.Add('PlanetSize',vtExternFun).VExternFun:=SF_PlanetSize;
  va.Add('PlanetCurInvention',vtExternFun).VExternFun:=SF_PlanetCurInvention;
  va.Add('PlanetCurInventionPoints',vtExternFun).VExternFun:=SF_PlanetCurInventionPoints;
  va.Add('PlanetInventionLevel',vtExternFun).VExternFun:=SF_PlanetInventionLevel;
  va.Add('PlanetBoostInventions',vtExternFun).VExternFun:=SF_PlanetBoostInventions;
  va.Add('PlanetWarriors',vtExternFun).VExternFun:=SF_PlanetWarriors;
  va.Add('GalaxySectors',vtExternFun).VExternFun:=SF_GalaxySectors;
  va.Add('GalaxyTechLevel',vtExternFun).VExternFun:=SF_GalaxyTechLevel;
  va.Add('GalaxyDominatorResearchPercent',vtExternFun).VExternFun:=SF_GalaxyDominatorResearchPercent;
  va.Add('GalaxyDominatorResearchMaterial',vtExternFun).VExternFun:=SF_GalaxyDominatorResearchMaterial;
  va.Add('GalaxyDiffLevels',vtExternFun).VExternFun:=SF_GalaxyDiffLevels;
  va.Add('SectorVisible',vtExternFun).VExternFun:=SF_SectorVisible;
  va.Add('HullHP',vtExternFun).VExternFun:=SF_HullHP;
  va.Add('HullDamageSuspectibility',vtExternFun).VExternFun:=SF_HullDamageSuspectibility;
  va.Add('HullType',vtExternFun).VExternFun:=SF_HullType;
  va.Add('HullSpecial',vtExternFun).VExternFun:=SF_HullSpecial;
  va.Add('HullSeries',vtExternFun).VExternFun:=SF_HullSeries;
  va.Add('GalaxyHoles',vtExternFun).VExternFun:=SF_GalaxyHoles;
  va.Add('HoleCreate2',vtExternFun).VExternFun:=SF_HoleCreate2;
  va.Add('HoleStar1',vtExternFun).VExternFun:=SF_HoleStar1;
  va.Add('HoleStar2',vtExternFun).VExternFun:=SF_HoleStar2;
  va.Add('HoleX1',vtExternFun).VExternFun:=SF_HoleX1;
  va.Add('HoleY1',vtExternFun).VExternFun:=SF_HoleY1;
  va.Add('HoleX2',vtExternFun).VExternFun:=SF_HoleX2;
  va.Add('HoleY2',vtExternFun).VExternFun:=SF_HoleY2;
  va.Add('HoleTurnCreate',vtExternFun).VExternFun:=SF_HoleTurnCreate;
  va.Add('HoleMap',vtExternFun).VExternFun:=SF_HoleMap;
  va.Add('StarRuins',vtExternFun).VExternFun:=SF_StarRuins;
  va.Add('CreateQuestItem',vtExternFun).VExternFun:=SF_CreateQuestItem;
  va.Add('ShipOrder',vtExternFun).VExternFun:=SF_ShipOrder;
  va.Add('ShipTurnBeforeEndOrder',vtExternFun).VExternFun:=SF_ShipTurnBeforeEndOrder;
  va.Add('ShipOrderData1',vtExternFun).VExternFun:=SF_ShipOrderData1;
  va.Add('ShipOrderData2',vtExternFun).VExternFun:=SF_ShipOrderData2;
  va.Add('ShipOrderObj',vtExternFun).VExternFun:=SF_ShipOrderObj;
  va.Add('ShipDestination',vtExternFun).VExternFun:=SF_ShipDestination;

  va.Add('BuildRuins',vtExternFun).VExternFun:=SF_BuildRuins;
  va.Add('BuildCustomRuins',vtExternFun).VExternFun:=SF_BuildCustomRuins;
  va.Add('RuinsChangeType',vtExternFun).VExternFun:=SF_RuinsChangeType;

  va.Add('ShipStanding',vtExternFun).VExternFun:=SF_ShipStanding;
  va.Add('ShipSlots',vtExternFun).VExternFun:=SF_ShipSlots;

  va.Add('MissileStar',vtExternFun).VExternFun:=SF_MissileStar;
  va.Add('MissileType',vtExternFun).VExternFun:=SF_MissileType;
  va.Add('CustomMissileType',vtExternFun).VExternFun:=SF_CustomMissileType;
  va.Add('MissileOwner',vtExternFun).VExternFun:=SF_MissileOwner;
  va.Add('MissileWeaponID',vtExternFun).VExternFun:=SF_MissileWeaponID;
  va.Add('MissileTarget',vtExternFun).VExternFun:=SF_MissileTarget;
  va.Add('MissileMaxDamage',vtExternFun).VExternFun:=SF_MissileMaxDamage;
  va.Add('MissileMinDamage',vtExternFun).VExternFun:=SF_MissileMinDamage;
  va.Add('MissileLive',vtExternFun).VExternFun:=SF_MissileLive;
  va.Add('MissileSpeed',vtExternFun).VExternFun:=SF_MissileSpeed;
  va.Add('MissileAngle',vtExternFun).VExternFun:=SF_MissileAngle;

  va.Add('AsteroidMinerals',vtExternFun).VExternFun:=SF_AsteroidMinerals;
  va.Add('AsteroidGraph',vtExternFun).VExternFun:=SF_AsteroidGraph;
  va.Add('AsteroidRespawn',vtExternFun).VExternFun:=SF_AsteroidRespawn;


  va.Add('ArrayAdd',vtExternFun).VExternFun:=SF_ArrayAdd;
  va.Add('ArrayDelete',vtExternFun).VExternFun:=SF_ArrayDelete;
  va.Add('ArrayClear',vtExternFun).VExternFun:=SF_ArrayClear;
  va.Add('ArrayDim',vtExternFun).VExternFun:=SF_ArrayDim;
  va.Add('ArraySort',vtExternFun).VExternFun:=SF_ArraySort;
  va.Add('ArraySortPartial',vtExternFun).VExternFun:=SF_ArraySortPartial;
  va.Add('ArrayRandomize',vtExternFun).VExternFun:=SF_ArrayRandomize;
  va.Add('ArrayFind',vtExternFun).VExternFun:=SF_ArrayFind;
  va.Add('ArrayFindInSorted',vtExternFun).VExternFun:=SF_ArrayFindInSorted;

  va.Add('DistToNearestEnemySystem',vtExternFun).VExternFun:=SF_DistToNearestEnemySystem;
  va.Add('StarEnemyThreatLevel',vtExternFun).VExternFun:=SF_StarEnemyThreatLevel;
  va.Add('BuildListOfQuestPossibleLocations',vtExternFun).VExternFun:=SF_BuildListOfQuestPossibleLocations;

  va.Add('FindItemInShip',vtExternFun).VExternFun:=SF_FindItemInShip;

  va.Add('GalaxyRangers',vtExternFun).VExternFun:=SF_GalaxyRangers;
  va.Add('MakeShipEnterStar',vtExternFun).VExternFun:=SF_MakeShipEnterStar;
  va.Add('ShipGetBad',vtExternFun).VExternFun:=SF_ShipGetBad;

  va.Add('ShipAddDropItem',vtExternFun).VExternFun:=SF_ShipAddDropItem;

  va.Add('OrderLock',vtExternFun).VExternFun:=SF_OrderLock;

  va.Add('BonusCount',vtExternFun).VExternFun:=SF_BonusCount;
  va.Add('SeriesCount',vtExternFun).VExternFun:=SF_SeriesCount;
  va.Add('BonusPriority',vtExternFun).VExternFun:=SF_BonusPriority;
  va.Add('BonusIsSpecial',vtExternFun).VExternFun:=SF_BonusIsSpecial;
  va.Add('BonusName',vtExternFun).VExternFun:=SF_BonusName;
  va.Add('BonusNumInCfg',vtExternFun).VExternFun:=SF_BonusNumInCfg;
  va.Add('SeriesNumInCfg',vtExternFun).VExternFun:=SF_SeriesNumInCfg;
  va.Add('BonusValue',vtExternFun).VExternFun:=SF_BonusValue;
  va.Add('FindBonusByName',vtExternFun).VExternFun:=SF_FindBonusByName;
  va.Add('FindSeriesByName',vtExternFun).VExternFun:=SF_FindSeriesByName;
  va.Add('FindBonusByCustomTag',vtExternFun).VExternFun:=SF_FindBonusByCustomTag;
  va.Add('FindBonusByNameInCfg',vtExternFun).VExternFun:=SF_FindBonusByNameInCfg;
  va.Add('BonusCustomTag',vtExternFun).VExternFun:=SF_BonusCustomTag;

  va.Add('CreateEquipmentWithSpecial',vtExternFun).VExternFun:=SF_CreateEquipmentWithSpecial;
  va.Add('SpecialToEquipment',vtExternFun).VExternFun:=SF_SpecialToEquipment;
  va.Add('ModuleToEquipment',vtExternFun).VExternFun:=SF_ModuleToEquipment;
  va.Add('EqSpecial',vtExternFun).VExternFun:=SF_EqSpecial;
  va.Add('EqModule',vtExternFun).VExternFun:=SF_EqModule;
  va.Add('MayAddBonusToEq',vtExternFun).VExternFun:=SF_MayAddBonusToEq;
  va.Add('BuildListOfMMByPriority',vtExternFun).VExternFun:=SF_BuildListOfMMByPriority;

  va.Add('BuildListOfNewShips',vtExternFun).VExternFun:=SF_BuildListOfNewShips;

  va.Add('PlanetToStar',vtExternFun).VExternFun:=SF_PlanetToStar;

  va.Add('Chameleon',vtExternFun).VExternFun:=SF_Chameleon;
  va.Add('IsChameleon',vtExternFun).VExternFun:=SF_IsChameleon;
  va.Add('PlayerChameleonCharges',vtExternFun).VExternFun:=SF_PlayerChameleonCharges;
  va.Add('PlayerChameleonCurType',vtExternFun).VExternFun:=SF_PlayerChameleonCurType;
  va.Add('PlayerChameleonDetected',vtExternFun).VExternFun:=SF_PlayerChameleonDetected;
  va.Add('PlayerLogicChameleon',vtExternFun).VExternFun:=SF_PlayerLogicChameleon;
  va.Add('SwitchToMirrorImage',vtExternFun).VExternFun:=SF_SwitchToMirrorImage;

  va.Add('EquipmentImageName',vtExternFun).VExternFun:=SF_EquipmentImageName;

  va.Add('StarFonImage',vtExternFun).VExternFun:=SF_StarFonImage;

  va.Add('ExtremalTakeOff',vtExternFun).VExternFun:=SF_ExtremalTakeOff;
  va.Add('ForceNextDay',vtExternFun).VExternFun:=SF_ForceNextDay;
  va.Add('ScriptActionsRun',vtExternFun).VExternFun:=SF_ScriptActionsRun;

  va.Add('StarListToPlanetList',vtExternFun).VExternFun:=SF_StarListToPlanetList;

  va.Add('EndGame',vtExternFun).VExternFun:=SF_EndGame;
  va.Add('CustomWin',vtExternFun).VExternFun:=SF_CustomWin;
  va.Add('CustomLose',vtExternFun).VExternFun:=SF_CustomLose;
  va.Add('PirateWin',vtExternFun).VExternFun:=SF_PirateWin;
  va.Add('StartVideo',vtExternFun).VExternFun:=SF_StartVideo;
  va.Add('StartMusic',vtExternFun).VExternFun:=SF_StartMusic;

  va.Add('NoComeKlingToStar',vtExternFun).VExternFun:=SF_NoComeKlingToStar;

  va.Add('NoDropToShip',vtExternFun).VExternFun:=SF_NoDropToShip;
  va.Add('NoTargetToShip',vtExternFun).VExternFun:=SF_NoTargetToShip;
  va.Add('NoTalkToShip',vtExternFun).VExternFun:=SF_NoTalkToShip;
  va.Add('NoScanToShip',vtExternFun).VExternFun:=SF_NoScanToShip;

  va.Add('NoJump',vtExternFun).VExternFun:=SF_NoJump;
  va.Add('NoLanding',vtExternFun).VExternFun:=SF_NoLanding;
  va.Add('NoShopUpdate',vtExternFun).VExternFun:=SF_NoShopUpdate;

  va.Add('NoDropItem',vtExternFun).VExternFun:=SF_NoDropItem;
  va.Add('CanSellItem',vtExternFun).VExternFun:=SF_CanSellItem;

  va.Add('TruceBetweenShips',vtExternFun).VExternFun:=SF_TruceBetweenShips;
  va.Add('ShipInPrison',vtExternFun).VExternFun:=SF_ShipInPrison;
  va.Add('ShipPartners',vtExternFun).VExternFun:=SF_ShipPartners;
  va.Add('PlayerPirates',vtExternFun).VExternFun:=SF_PlayerPirates;
  va.Add('ShipIsPartner',vtExternFun).VExternFun:=SF_ShipIsPartner;
  va.Add('ShipFreeSpace',vtExternFun).VExternFun:=SF_ShipFreeSpace;
  va.Add('ShipWealth',vtExternFun).VExternFun:=SF_ShipWealth;
  va.Add('DomiksDefeated',vtExternFun).VExternFun:=SF_DomiksDefeated;
  va.Add('CoalitionDefeated',vtExternFun).VExternFun:=SF_CoalitionDefeated;
  va.Add('ShipRefuel',vtExternFun).VExternFun:=SF_ShipRefuel;
  va.Add('ShipRepairEq',vtExternFun).VExternFun:=SF_ShipRepairEq;
  va.Add('ItemInScript',vtExternFun).VExternFun:=SF_ItemInScript;
  va.Add('FindPlanetByAdvancement',vtExternFun).VExternFun:=SF_FindPlanetByAdvancement;
  va.Add('StarListToTransitPlanetList',vtExternFun).VExternFun:=SF_StarListToTransitPlanetList;

  va.Add('GalaxyEvents',vtExternFun).VExternFun:=SF_GalaxyEvents;
  va.Add('GalaxyEventDate',vtExternFun).VExternFun:=SF_GalaxyEventDate;
  va.Add('GalaxyEventType',vtExternFun).VExternFun:=SF_GalaxyEventType;
  va.Add('GalaxyEventData',vtExternFun).VExternFun:=SF_GalaxyEventData;
  va.Add('GalaxyEventsTextData',vtExternFun).VExternFun:=SF_GalaxyEventsTextData;

  va.Add('PlanetNews',vtExternFun).VExternFun:=SF_PlanetNews;
  va.Add('PlanetNewsDate',vtExternFun).VExternFun:=SF_PlanetNewsDate;
  va.Add('PlanetNewsType',vtExternFun).VExternFun:=SF_PlanetNewsType;
  va.Add('PlanetNewsText',vtExternFun).VExternFun:=SF_PlanetNewsText;

  va.Add('ControlledSystems',vtExternFun).VExternFun:=SF_ControlledSystems;

  va.Add('ShipInFear',vtExternFun).VExternFun:=SF_ShipInFear;

  va.Add('CreateGoods',vtExternFun).VExternFun:=SF_CreateGoods;
  va.Add('GetNodesFromShip',vtExternFun).VExternFun:=SF_GetNodesFromShip;
  va.Add('GetNodesFromStorage',vtExternFun).VExternFun:=SF_GetNodesFromStorage;
  va.Add('RangerBaseNodes',vtExternFun).VExternFun:=SF_RangerBaseNodes;

  va.Add('RuinsAllowModernization',vtExternFun).VExternFun:=SF_RuinsAllowModernization;
  va.Add('RuinsMicromoduleChain',vtExternFun).VExternFun:=SF_RuinsMicromoduleChain;

  va.Add('DomikKilledInCurSystem',vtExternFun).VExternFun:=SF_DomikKilledInCurSystem;

  va.Add('ShipTypeN',vtExternFun).VExternFun:=SF_ShipTypeN;
  va.Add('ShipSubType',vtExternFun).VExternFun:=SF_ShipSubType;

  va.Add('ShipChangeStar',vtExternFun).VExternFun:=SF_ShipChangeStar;

  va.Add('IsFilm',vtExternFun).VExternFun:=SF_IsFilm;
  va.Add('FilmFlags',vtExternFun).VExternFun:=SF_FilmFlags;
  va.Add('ShowEffect',vtExternFun).VExternFun:=SF_ShowEffect;
  va.Add('ShowStaticEffect',vtExternFun).VExternFun:=SF_ShowStaticEffect;
  va.Add('FilmSound',vtExternFun).VExternFun:=SF_FilmSound;

  va.Add('FireWeapon',vtExternFun).VExternFun:=SF_FireWeapon;
  va.Add('WeaponHit',vtExternFun).VExternFun:=SF_WeaponHit;
  va.Add('DealDamageToShip',vtExternFun).VExternFun:=SF_DealDamageToShip;
  va.Add('LaunchMissile',vtExternFun).VExternFun:=SF_LaunchMissile;
  va.Add('SpawnMissile',vtExternFun).VExternFun:=SF_SpawnMissile;

  va.Add('BonusText',vtExternFun).VExternFun:=SF_BonusText;

  va.Add('PlanetPirateClan',vtExternFun).VExternFun:=SF_PlanetPirateClan;
  va.Add('Blazer',vtExternFun).VExternFun:=SF_Blazer;
  va.Add('Keller',vtExternFun).VExternFun:=SF_Keller;
  va.Add('Terron',vtExternFun).VExternFun:=SF_Terron;

  va.Add('PirateType',vtExternFun).VExternFun:=SF_PirateType;
  va.Add('PlayerQuestInProgress',vtExternFun).VExternFun:=SF_PlayerQuestInProgress;
  va.Add('PlayerQuestsCompleted',vtExternFun).VExternFun:=SF_PlayerQuestsCompleted;
  va.Add('QuestsStatusByNom',vtExternFun).VExternFun:=SF_QuestsStatusByNom;
  va.Add('PlayerPlanetaryBattlesCompleted',vtExternFun).VExternFun:=SF_PlayerPlanetaryBattlesCompleted;
  va.Add('PlayerMayTakeSubCrack',vtExternFun).VExternFun:=SF_PlayerMayTakeSubCrack;
  va.Add('SubCrackCost',vtExternFun).VExternFun:=SF_SubCrackCost;
  va.Add('ShipCalcParam',vtExternFun).VExternFun:=SF_ShipCalcParam;
  va.Add('ShipRefit',vtExternFun).VExternFun:=SF_ShipRefit;
  va.Add('ShipImproveItems',vtExternFun).VExternFun:=SF_ShipImproveItems;
  va.Add('ItemImprovement',vtExternFun).VExternFun:=SF_ItemImprovement;
  va.Add('ShipFreeFlight',vtExternFun).VExternFun:=SF_ShipFreeFlight;
  va.Add('ShipKillFactionInCurSystem',vtExternFun).VExternFun:=SF_ShipKillFactionInCurSystem;
  va.Add('CapitalShipStats',vtExternFun).VExternFun:=SF_CapitalShipStats;
  va.Add('PlayerBridge',vtExternFun).VExternFun:=SF_PlayerBridge;


  va.Add('PlayerDebt',vtExternFun).VExternFun:=SF_PlayerDebt;
  va.Add('PlayerDebtDate',vtExternFun).VExternFun:=SF_PlayerDebtDate;
  va.Add('PlayerDebtCnt',vtExternFun).VExternFun:=SF_PlayerDebtCnt;
  va.Add('PlayerDeposit',vtExternFun).VExternFun:=SF_PlayerDeposit;
  va.Add('PlayerDepositDate',vtExternFun).VExternFun:=SF_PlayerDepositDate;
  va.Add('PlayerDepositDay',vtExternFun).VExternFun:=SF_PlayerDepositDay;
  va.Add('PlayerDepositPercent',vtExternFun).VExternFun:=SF_PlayerDepositPercent;
  va.Add('PlayerMedPolicy',vtExternFun).VExternFun:=SF_PlayerMedPolicy;

  va.Add('ShipCustomShipInfosCount',vtExternFun).VExternFun:=SF_ShipCustomShipInfosCount;
  va.Add('ShipAddCustomShipInfo',vtExternFun).VExternFun:=SF_ShipAddCustomShipInfo;
  va.Add('ShipDeleteCustomShipInfo',vtExternFun).VExternFun:=SF_ShipDeleteCustomShipInfo;
  va.Add('ShipFindCustomShipInfoByType',vtExternFun).VExternFun:=SF_ShipFindCustomShipInfoByType;
  va.Add('ShipCustomShipInfoDescription',vtExternFun).VExternFun:=SF_ShipCustomShipInfoDescription;
  va.Add('ShipCustomShipInfoData',vtExternFun).VExternFun:=SF_ShipCustomShipInfoData;
  va.Add('ShipCustomShipInfoTextData',vtExternFun).VExternFun:=SF_ShipCustomShipInfoTextData;

  va.Add('StarCustomStarInfosCount',vtExternFun).VExternFun:=SF_StarCustomStarInfosCount;
  va.Add('StarAddCustomStarInfo',vtExternFun).VExternFun:=SF_StarAddCustomStarInfo;
  va.Add('StarDeleteCustomStarInfo',vtExternFun).VExternFun:=SF_StarDeleteCustomStarInfo;
  va.Add('StarFindCustomStarInfoByType',vtExternFun).VExternFun:=SF_StarFindCustomStarInfoByType;
  va.Add('StarCustomStarInfoData',vtExternFun).VExternFun:=SF_StarCustomStarInfoData;

  va.Add('ItemCanBeBroken',vtExternFun).VExternFun:=SF_ItemCanBeBroken;
  va.Add('ItemFragility',vtExternFun).VExternFun:=SF_ItemFragility;
  va.Add('ItemDurability',vtExternFun).VExternFun:=SF_ItemDurability;
  va.Add('ItemLevel',vtExternFun).VExternFun:=SF_ItemLevel;
  va.Add('ContainerFuel',vtExternFun).VExternFun:=SF_ContainerFuel;
  va.Add('ItemCharge',vtExternFun).VExternFun:=SF_ItemCharge;
  va.Add('MissilesToRearm',vtExternFun).VExternFun:=SF_MissilesToRearm;
  va.Add('WeaponAmmunition',vtExternFun).VExternFun:=SF_WeaponAmmunition;
  va.Add('WeaponMaxAmmunition',vtExternFun).VExternFun:=SF_WeaponMaxAmmunition;
  va.Add('ShipSpecialBonuses',vtExternFun).VExternFun:=SF_ShipSpecialBonuses;

  va.Add('ItemExtraSpecials',vtExternFun).VExternFun:=SF_ItemExtraSpecials;
  va.Add('ItemExtraSpecialsCountByType',vtExternFun).VExternFun:=SF_ItemExtraSpecialsCountByType;
  va.Add('ItemExtraSpecialsAddByType',vtExternFun).VExternFun:=SF_ItemExtraSpecialsAddByType;
  va.Add('ItemExtraSpecialsDeleteByType',vtExternFun).VExternFun:=SF_ItemExtraSpecialsDeleteByType;

  va.Add('ExecuteCodeFromString',vtExternFun).VExternFun:=SF_ExecuteCodeFromString;
  va.Add('GenerateCodeStringFromBlock',vtExternFun).VExternFun:=SF_GenerateCodeStringFromBlock;
  va.Add('ItemOnUseCode',vtExternFun).VExternFun:=SF_ItemOnUseCode;
  va.Add('ItemOnActCode',vtExternFun).VExternFun:=SF_ItemOnActCode;
  va.Add('CreateActCodeEvent',vtExternFun).VExternFun:=SF_CreateActCodeEvent;
  va.Add('CurItem',vtExternFun).VExternFun:=SF_CurItem;
  va.Add('CurInfo',vtExternFun).VExternFun:=SF_CurInfo;
  va.Add('ScriptItemActShip',vtExternFun).VExternFun:=SF_ScriptItemActShip;
  va.Add('ScriptItemActObject1',vtExternFun).VExternFun:=SF_ScriptItemActObject1;
  va.Add('ScriptItemActObject2',vtExternFun).VExternFun:=SF_ScriptItemActObject2;
  va.Add('ScriptItemActParam',vtExternFun).VExternFun:=SF_ScriptItemActParam;
  va.Add('ScriptItemActionType',vtExternFun).VExternFun:=SF_ScriptItemActionType;

  va.Add('OnUseCodeTranclucator',vtExternFun).VExternFun:=SF_OnUseCodeTranclucator;
  va.Add('OnUseCodeTransmitter',vtExternFun).VExternFun:=SF_OnUseCodeTransmitter;
  va.Add('OnUseCodeBlackHole',vtExternFun).VExternFun:=SF_OnUseCodeBlackHole;
  va.Add('OnUseCodeMissileDef',vtExternFun).VExternFun:=SF_OnUseCodeMissileDef;
  va.Add('MessageBox',vtExternFun).VExternFun:=SF_MessageBox;
  va.Add('MessageBoxYesNo',vtExternFun).VExternFun:=SF_MessageBoxYesNo;
  va.Add('CountBox',vtExternFun).VExternFun:=SF_CountBox;
  va.Add('NumberBox',vtExternFun).VExternFun:=SF_NumberBox;
  va.Add('TextBox',vtExternFun).VExternFun:=SF_TextBox;
  va.Add('ListBox',vtExternFun).VExternFun:=SF_ListBox;
  va.Add('FormCurShip',vtExternFun).VExternFun:=SF_FormCurShip;
  va.Add('UselessItemText',vtExternFun).VExternFun:=SF_UselessItemText;
  va.Add('UselessItemData',vtExternFun).VExternFun:=SF_UselessItemData;



  va.Add('GetAchievementSHU',vtExternFun).VExternFun:=SF_GetAchievementSHU;
  va.Add('GetAchievementGIRLSHIRE',vtExternFun).VExternFun:=SF_GetAchievementGIRLSHIRE;
  va.Add('GetAchievementGIRLSQUEST',vtExternFun).VExternFun:=SF_GetAchievementGIRLSQUEST;
  va.Add('GetAchievementPIRATEWIN',vtExternFun).VExternFun:=SF_GetAchievementPIRATEWIN;
  va.Add('GetAchievementCOALLITION',vtExternFun).VExternFun:=SF_GetAchievementCOALLITION;
  va.Add('GetAchievementHULL',vtExternFun).VExternFun:=SF_GetAchievementHULL;

  va.Add('UICheckElement',vtExternFun).VExternFun:=SF_UICheckElement;

  va.Add('InterfaceState',vtExternFun).VExternFun:=SF_InterfaceState;
  va.Add('InterfaceText',vtExternFun).VExternFun:=SF_InterfaceText;
  va.Add('InterfaceImage',vtExternFun).VExternFun:=SF_InterfaceImage;
  va.Add('InterfacePos',vtExternFun).VExternFun:=SF_InterfacePos;
  va.Add('InterfaceSize',vtExternFun).VExternFun:=SF_InterfaceSize;

  va.Add('ButtonClick',vtExternFun).VExternFun:=SF_ButtonClick;
  va.Add('SetFocus',vtExternFun).VExternFun:=SF_SetFocus;
  va.Add('CurrentForm',vtExternFun).VExternFun:=SF_CurrentForm;
  va.Add('FormShipCurItem',vtExternFun).VExternFun:=SF_FormShipCurItem;
  va.Add('UpdateFormShip',vtExternFun).VExternFun:=SF_UpdateFormShip;
  va.Add('FormChange',vtExternFun).VExternFun:=SF_FormChange;
  va.Add('RunChildForm',vtExternFun).VExternFun:=SF_RunChildForm;

  va.Add('OpenCustomForm',vtExternFun).VExternFun:=SF_OpenCustomForm;
  va.Add('CloseCustomForm',vtExternFun).VExternFun:=SF_CloseCustomForm;
  va.Add('CustomInterfaceState',vtExternFun).VExternFun:=SF_CustomInterfaceState;
  va.Add('CustomInterfaceText',vtExternFun).VExternFun:=SF_CustomInterfaceText;
  va.Add('CustomInterfaceImage',vtExternFun).VExternFun:=SF_CustomInterfaceImage;
  va.Add('CustomInterfacePos',vtExternFun).VExternFun:=SF_CustomInterfacePos;
  va.Add('CustomInterfacePosZ',vtExternFun).VExternFun:=SF_CustomInterfacePosZ;
  va.Add('CustomInterfaceSize',vtExternFun).VExternFun:=SF_CustomInterfaceSize;



  va.Add('StarMapCenterView',vtExternFun).VExternFun:=SF_StarMapCenterView;
  va.Add('StarMapCurPosX',vtExternFun).VExternFun:=SF_StarMapCurPosX;
  va.Add('StarMapCurPosY',vtExternFun).VExternFun:=SF_StarMapCurPosY;

  va.Add('CustomWeaponTypes',vtExternFun).VExternFun:=SF_CustomWeaponTypes;
  va.Add('InventNewCustomWeapon',vtExternFun).VExternFun:=SF_InventNewCustomWeapon;
  va.Add('GetCustomWeaponInfo',vtExternFun).VExternFun:=SF_GetCustomWeaponInfo;
  va.Add('GetCustomWeaponData',vtExternFun).VExternFun:=SF_GetCustomWeaponData;
  va.Add('GetCustomWeaponPrimaryDamageType',vtExternFun).VExternFun:=SF_GetCustomWeaponPrimaryDamageType;
  va.Add('SetCustomWeaponAvailability',vtExternFun).VExternFun:=SF_SetCustomWeaponAvailability;
  va.Add('SetCustomWeaponSE',vtExternFun).VExternFun:=SF_SetCustomWeaponSE;
  va.Add('SetCustomWeaponPrimaryData',vtExternFun).VExternFun:=SF_SetCustomWeaponPrimaryData;
  va.Add('SetCustomWeaponSizeAndCost',vtExternFun).VExternFun:=SF_SetCustomWeaponSizeAndCost;
  va.Add('SetCustomWeaponDamageData',vtExternFun).VExternFun:=SF_SetCustomWeaponDamageData;
  va.Add('SetCustomWeaponShotData',vtExternFun).VExternFun:=SF_SetCustomWeaponShotData;
  va.Add('SetCustomMissileWeaponStats',vtExternFun).VExternFun:=SF_SetCustomMissileWeaponStats;

  va.Add('StarCustomFaction',vtExternFun).VExternFun:=SF_StarCustomFaction;
  va.Add('ShipCustomFaction',vtExternFun).VExternFun:=SF_ShipCustomFaction;
  va.Add('EqCustomFaction',vtExternFun).VExternFun:=SF_EqCustomFaction;
  
  va.Add('ImportedFunction',vtExternFun).VExternFun:=SF_ImportedFunction;
  va.Add('ImportAll',vtExternFun).VExternFun:=SF_ImportAll;

  va.Add('GalaxyPtr',vtExternFun).VExternFun:=SF_GalaxyPtr;

  va.Add('t_ArtDefToEnergy',vtInt).VInt:=integer(t_ArtDefToEnergy);
  va.Add('t_ArtEnergyPulse',vtInt).VInt:=integer(t_ArtEnergyPulse);
  va.Add('t_ArtEnergyDef',vtInt).VInt:=integer(t_ArtEnergyDef);
  va.Add('t_ArtSplinter',vtInt).VInt:=integer(t_ArtSplinter);
  va.Add('t_ArtDecelerate',vtInt).VInt:=integer(t_ArtDecelerate);
  va.Add('t_ArtMissileDef',vtInt).VInt:=integer(t_ArtMissileDef);
  va.Add('t_ArtForsage',vtInt).VInt:=integer(t_ArtForsage);
  va.Add('t_ArtWeaponToSpeed',vtInt).VInt:=integer(t_ArtWeaponToSpeed);
  va.Add('t_ArtGiperJump',vtInt).VInt:=integer(t_ArtGiperJump);
  va.Add('t_ArtBlackHole',vtInt).VInt:=integer(t_ArtBlackHole);
  va.Add('t_ArtDefToArms1',vtInt).VInt:=integer(t_ArtDefToArms1);
  va.Add('t_ArtDefToArms2',vtInt).VInt:=integer(t_ArtDefToArms2);
  va.Add('t_ArtArtefactor',vtInt).VInt:=integer(t_ArtArtefactor);
  va.Add('t_ArtBio',vtInt).VInt:=integer(t_ArtBio);
  va.Add('t_ArtPDTurret',vtInt).VInt:=integer(t_ArtPDTurret);
  va.Add('t_ArtFastRacks',vtInt).VInt:=integer(t_ArtFastRacks);

  va.Add('t_Cistern',vtInt).VInt:=integer(t_Cistern);
  va.Add('t_Satellite',vtInt).VInt:=integer(t_Satellite);
  va.Add('t_MicroModule',vtInt).VInt:=integer(t_MicroModule);
  va.Add('t_UselessCountableItem',vtInt).VInt:=integer(t_UselessCountableItem);

  //va.Add('TalkPlayer',vtInt).VInt:=integer(TalkPlayer);
  va.Add('TalkMoney',vtInt).VInt:=integer(TalkMoney);
  va.Add('TalkGoods',vtInt).VInt:=integer(TalkGoods);
  va.Add('TalkTruce',vtInt).VInt:=integer(TalkTruce);
  va.Add('TalkAttack',vtInt).VInt:=integer(TalkAttack);
  va.Add('TalkBreakPartner',vtInt).VInt:=integer(TalkBreakPartner);
  va.Add('TalkPartnerTheEnd',vtInt).VInt:=integer(TalkPartnerTheEnd);
  va.Add('TalkPartnerRiot',vtInt).VInt:=integer(TalkPartnerRiot);

  va.Add('bonHull',vtInt).VInt:=integer(bonHull);
  va.Add('bonFuel',vtInt).VInt:=integer(bonFuel);
  va.Add('bonSpeed',vtInt).VInt:=integer(bonSpeed);
  va.Add('bonJump',vtInt).VInt:=integer(bonJump);
  va.Add('bonRadar',vtInt).VInt:=integer(bonRadar);
  va.Add('bonScan',vtInt).VInt:=integer(bonScan);
  va.Add('bonDroid',vtInt).VInt:=integer(bonDroid);
  va.Add('bonHook',vtInt).VInt:=integer(bonHook);
  va.Add('bonDef',vtInt).VInt:=integer(bonDef);
  va.Add('bonWEnergy',vtInt).VInt:=integer(bonWEnergy);
  va.Add('bonWSplinter',vtInt).VInt:=integer(bonWSplinter);
  va.Add('bonWMissile',vtInt).VInt:=integer(bonWMissile);
  va.Add('bonWRadius',vtInt).VInt:=integer(bonWRadius);
  va.Add('bonSlotRadar',vtInt).VInt:=integer(bonSlotRadar);
  va.Add('bonSlotScaner',vtInt).VInt:=integer(bonSlotScaner);
  va.Add('bonSlotDroid',vtInt).VInt:=integer(bonSlotDroid);
  va.Add('bonSlotHook',vtInt).VInt:=integer(bonSlotHook);
  va.Add('bonSlotDef',vtInt).VInt:=integer(bonSlotDef);
  va.Add('bonSlotWeapon',vtInt).VInt:=integer(bonSlotWeapon);
  va.Add('bonSlotArt',vtInt).VInt:=integer(bonSlotArt);
  va.Add('bonSlotForsage',vtInt).VInt:=integer(bonSlotForsage);
  va.Add('bonHookRadius',vtInt).VInt:=integer(bonHookRadius);
  va.Add('bonSkill1',vtInt).VInt:=integer(bonSkill1);
  va.Add('bonSkill2',vtInt).VInt:=integer(bonSkill2);
  va.Add('bonSkill3',vtInt).VInt:=integer(bonSkill3);
  va.Add('bonSkill4',vtInt).VInt:=integer(bonSkill4);
  va.Add('bonSkill5',vtInt).VInt:=integer(bonSkill5);
  va.Add('bonSkill6',vtInt).VInt:=integer(bonSkill6);
  va.Add('bonMass',vtInt).VInt:=integer(bonMass);
  va.Add('bonExtraAkrinEff',vtInt).VInt:=integer(bonExtraAkrinEff);
  va.Add('bonExtraAkrinPenalty',vtInt).VInt:=integer(bonExtraAkrinPenalty);
  va.Add('bonAmmo',vtInt).VInt:=integer(bonAmmo);
  va.Add('bonShots',vtInt).VInt:=integer(bonShots);
  va.Add('bonMissileSpeed',vtInt).VInt:=integer(bonMissileSpeed);
  va.Add('bonShotSpeed',vtInt).VInt:=integer(bonShotSpeed);
  va.Add('bonHookMaxSpeed',vtInt).VInt:=integer(bonHookMaxSpeed);
  va.Add('bonHookMinSpeed',vtInt).VInt:=integer(bonHookMinSpeed);
  va.Add('bonStimCapacity',vtInt).VInt:=integer(bonStimCapacity);
  va.Add('bonZonds',vtInt).VInt:=integer(bonZonds);
  va.Add('bonAttacks',vtInt).VInt:=integer(bonAttacks);
  va.Add('bonResistAsteroid',vtInt).VInt:=integer(bonResistAsteroid);

  for act:=low(act) to high(act) do va.Add(ActionTypeStr[act],vtInt).VInt:=integer(act);

  GScriptThread:=TScriptThread.Create;
  GScriptThread.SetPriority(tpLower);

  GScriptActCodeItem:=TList.Create;
  GScriptActCodeInfo:=TList.Create;

  GScriptActCodeShip:=TList.Create;
  GScriptActCodeObject1:=TList.Create;
  GScriptActCodeObject2:=TList.Create;
  GScriptActCodeParam:=TList.Create;
  GScriptActCodeType:=TList.Create;

  GScriptsThatCalledTQ:=TList.Create;
  GScriptsThatCalledAB:=TList.Create;
  GScriptsThatCalledPB:=TList.Create;
  GScriptsThatCalledVD:=TList.Create;
  GABShipsForScriptAB:=TObjectList.Create;
end;

end.

