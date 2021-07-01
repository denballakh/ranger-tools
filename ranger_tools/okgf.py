import sys
import os
import ctypes

# from gi import GI

__all__ = ['OKGF']

class OKGF:
    def __init__(self):
        self.lib = ctypes.cdll.LoadLibrary('.\\okgf.dll')

okgf = OKGF()
print(okgf.lib)
print(okgf.lib.OKGR_TransBuf_BuildFromRGBA_16)

# def TGraphBuf_BuildGI_Alpha(bd: TBufEC, autosize: bool):
#     len: int
#     zag: SGIZag
#     zagunit: SGIUnit
#     tb: TBufEC

#     bd.Clear;

#     SwapChannels(0,2);

#     tb:=TBufEC.Create;

#     ZeroMemory(@zag,sizeof(SGIZag));
#     zag.id0:=Ord('g');
#     zag.id1:=Ord('i');
#     zag.id2:=0;
#     zag.id3:=0;
#     zag.ver:=1;
#     zag.rect.Left:=0;
#     zag.rect.Top:=0;
#     zag.rect.Right:=0;
#     zag.rect.Bottom:=0;
#     zag.mR:=$00000F800;
#     zag.mG:=$0000007E0;
#     zag.mB:=$00000001F;
#     zag.mA:=$000000000;
#     zag.format:=2;
#     zag.countUnit:=3;
#     zag.countUpdateRect:=0;
#     zag.smeUpdateRect:=0;
#     bd.Add(@zag,sizeof(SGIZag));

#     ZeroMemory(@zagunit,sizeof(SGIUnit));
#     bd.Add(@zagunit,sizeof(SGIUnit));
#     bd.Add(@zagunit,sizeof(SGIUnit));
#     bd.Add(@zagunit,sizeof(SGIUnit));

#     if ((zagunit.rect.Right-zagunit.rect.Left)>0) and ((zagunit.rect.Right-zagunit.rect.Left)>0) then begin
#         len:=OKGR_TransBuf_BuildFromRGBA_16(PixelBuf(zagunit.rect.left,zagunit.rect.top),FLenLine,zagunit.rect.Right-zagunit.rect.Left,zagunit.rect.Bottom-zagunit.rect.Top,nil);
#         OKGR_TransBuf_BuildFromRGBA_16(PixelBuf(zagunit.rect.left,zagunit.rect.top),FLenLine,zagunit.rect.Right-zagunit.rect.Left,zagunit.rect.Bottom-zagunit.rect.Top,tb.Buf);
#         zagunit.sme:=bd.Pointer;
#         zagunit.size:=len;
#         zagunit.rect.Left:=zagunit.rect.Left+FPos.x;
#         zagunit.rect.Top:=zagunit.rect.Top+FPos.y;
#         zagunit.rect.Right:=zagunit.rect.Right+FPos.x;
#         zagunit.rect.Bottom:=zagunit.rect.Bottom+FPos.y;
#         bd.Add(tb.Buf,len);
#         bd.S(sizeof(SGIZag)+sizeof(SGIUnit)*0,@zagunit,sizeof(SGIUnit));

#         zag.rect:=zagunit.rect;
#     end;

#     if autosize then zagunit.rect:=OCutOffAlphaCalc_TransAlphaBuf_BuildFromRGBA_16(self)
#     else begin zagunit.rect.TopLeft:=Point(0,0); zagunit.rect.BottomRight:=Point(FLenX,FLenY); end;
#     if ((zagunit.rect.Right-zagunit.rect.Left)>0) and ((zagunit.rect.Right-zagunit.rect.Left)>0) then begin
#         len:=OKGR_TransAlphaBuf_BuildFromRGBA_16(PixelBuf(zagunit.rect.left,zagunit.rect.top),FLenLine,zagunit.rect.Right-zagunit.rect.Left,zagunit.rect.Bottom-zagunit.rect.Top,nil);
#         if len<1 then raise Exception.Create('Error save file.');
#         tb.Len:=len;
#         OKGR_TransAlphaBuf_BuildFromRGBA_16(PixelBuf(zagunit.rect.left,zagunit.rect.top),FLenLine,zagunit.rect.Right-zagunit.rect.Left,zagunit.rect.Bottom-zagunit.rect.Top,tb.Buf);
#         zagunit.sme:=bd.Pointer;
#         zagunit.size:=len;
#         zagunit.rect.Left:=zagunit.rect.Left+FPos.x;
#         zagunit.rect.Top:=zagunit.rect.Top+FPos.y;
#         zagunit.rect.Right:=zagunit.rect.Right+FPos.x;
#         zagunit.rect.Bottom:=zagunit.rect.Bottom+FPos.y;
#         bd.Add(tb.Buf,len);
#         bd.S(sizeof(SGIZag)+sizeof(SGIUnit)*1,@zagunit,sizeof(SGIUnit));

#         if ((zag.rect.right-zag.rect.left)<1) or ((zag.rect.bottom-zag.rect.top)<1) then begin
#             zag.rect:=zagunit.rect;
#         end else begin
#             UnionRect(zag.rect,zag.rect,zagunit.rect);
#         end;
#     end;

#     if autosize then zagunit.rect:=OCutOffAlphaCalc_TransAlphaBuf_BuildFromRGBA_16(self)
#     else begin zagunit.rect.TopLeft:=Point(0,0); zagunit.rect.BottomRight:=Point(FLenX,FLenY); end;
#     if ((zagunit.rect.Right-zagunit.rect.Left)>0) and ((zagunit.rect.Right-zagunit.rect.Left)>0) then begin
#         len:=OKGR_AlphaBuf_BuildFromRGBA(PixelBuf(zagunit.rect.left,zagunit.rect.top),FLenLine,zagunit.rect.Right-zagunit.rect.Left,zagunit.rect.Bottom-zagunit.rect.Top,nil);
#         if len<1 then raise Exception.Create('Error save file.');
#         tb.Len:=len;
#         OKGR_AlphaBuf_BuildFromRGBA(PixelBuf(zagunit.rect.left,zagunit.rect.top),FLenLine,zagunit.rect.Right-zagunit.rect.Left,zagunit.rect.Bottom-zagunit.rect.Top,tb.Buf);
#         zagunit.sme:=bd.Pointer;
#         zagunit.size:=len;
#         zagunit.rect.Left:=zagunit.rect.Left+FPos.x;
#         zagunit.rect.Top:=zagunit.rect.Top+FPos.y;
#         zagunit.rect.Right:=zagunit.rect.Right+FPos.x;
#         zagunit.rect.Bottom:=zagunit.rect.Bottom+FPos.y;
#         bd.Add(tb.Buf,len);
#         bd.S(sizeof(SGIZag)+sizeof(SGIUnit)*2,@zagunit,sizeof(SGIUnit));

#         if ((zag.rect.right-zag.rect.left)<1) or ((zag.rect.bottom-zag.rect.top)<1) then begin
#             zag.rect:=zagunit.rect;
#         end else begin
#             UnionRect(zag.rect,zag.rect,zagunit.rect);
#         end;
#     end;

#     bd.S(0,@zag,sizeof(SGIZag));

#     tb.Free;

#     SwapChannels(0,2);
# end;
