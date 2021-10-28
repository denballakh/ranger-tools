library FGIntWrapper;


uses
  Windows,
  System.SysUtils,
  System.Classes,
  FGInt in 'FGInt\\FGInt.pas';

type ByteP = ^byte;

function AddIntegers(const _a, _b: integer): integer; cdecl;
begin
  result := _a + _b;
end;
exports AddIntegers;

function _ConvertBase64to256(aaa: pstring): integer; cdecl;
var 
  s1, s2, tmp, res: string;
begin
  res := '';

  s1 := 'HjwH94fmhClFC1prPy';
  s2 := 'DjAVRGx=';

  ConvertBase64to256(s1, tmp);
  res := res + tmp;
  res := res + '<<<>>>';
  ConvertBase64to256(s2, tmp);
  res := res + tmp;

  aaa^ := res;
  // SetLength(aaa^, 255);
  // strcopy(@aaa, @res);
end;

exports _ConvertBase64to256;

begin
end.
