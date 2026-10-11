import ctypes,hashlib,json,struct,tempfile
from pathlib import Path

def exercise(lib):
 lib.chd_open.argtypes=[ctypes.c_char_p,ctypes.c_int,ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p)];lib.chd_open.restype=ctypes.c_int
 lib.chd_close.argtypes=[ctypes.c_void_p];lib.chd_close.restype=None
 lib.chd_read.argtypes=[ctypes.c_void_p,ctypes.c_uint32,ctypes.c_void_p];lib.chd_read.restype=ctypes.c_int
 lib.chd_get_metadata.argtypes=[ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_uint32,ctypes.POINTER(ctypes.c_uint32),ctypes.POINTER(ctypes.c_uint32),ctypes.POINTER(ctypes.c_uint8)];lib.chd_get_metadata.restype=ctypes.c_int
 tag=int.from_bytes(b'GDDD','big');results=[]
 with tempfile.TemporaryDirectory() as temporary:
  for version,cylinders,bps in [(1,1,512),(1,2147483647,512),(2,1,4096),(2,2147483648,512)]:
   length=76 if version==1 else 80
   header=bytearray(length);header[:8]=b'MComprHD'
   for offset,value in [(8,length),(12,version),(16,0),(20,0),(24,1),(28,1),(32,cylinders),(36,1),(40,1)]:struct.pack_into('>I',header,offset,value)
   if version==2:struct.pack_into('>I',header,76,bps)
   payload=bytes(range(256))*(bps//256);offset=length+16
   raw=bytes(header)+struct.pack('>Q',(bps<<44)|offset)+b'EndOfLis'+payload
   path=Path(temporary)/f'v{version}-{cylinders}.chd';path.write_bytes(raw);handle=ctypes.c_void_p();rc=lib.chd_open(bytes(path),1,None,ctypes.byref(handle));assert rc==0,(version,cylinders,rc)
   try:
    expected=f'CYLS:{ctypes.c_int32(cylinders).value},HEADS:1,SECS:1,BPS:{bps}'.encode()+b'\0'
    output=ctypes.create_string_buffer(b'Z'*80);n=ctypes.c_uint32();actualtag=ctypes.c_uint32();flags=ctypes.c_uint8()
    rc=lib.chd_get_metadata(handle,tag,0,output,80,ctypes.byref(n),ctypes.byref(actualtag),ctypes.byref(flags));assert rc==0 and n.value==len(expected) and actualtag.value==tag
    assert output.raw[:len(expected)]==expected and output.raw[len(expected):80]==b'Z'*(80-len(expected))
    short=ctypes.create_string_buffer(b'Z'*80)
    assert lib.chd_get_metadata(handle,tag,0,short,3,ctypes.byref(n),None,None)==0
    assert short.raw[:3]==expected[:3] and short.raw[3:80]==b'Z'*77 and n.value==len(expected)
    assert lib.chd_get_metadata(handle,tag,1,output,80,None,None,None)!=0
    block=ctypes.create_string_buffer(bps);assert lib.chd_read(handle,0,block)==0 and block.raw==payload
    results.append({'version':version,'cylinders':cylinders,'bytes_per_sector':bps,'fixture_sha256':hashlib.sha256(raw).hexdigest(),'metadata_hex':expected.hex(),'full_metadata':True,'bounded_short_copy_canary':True,'absent_index_refused':True,'hunk_bytes_equal':True})
   finally:lib.chd_close(handle)
  bad=Path(temporary)/'invalid.chd';bad.write_bytes(b'NotA_CHD'+b'\0'*80);handle=ctypes.c_void_p();assert lib.chd_open(bytes(bad),1,None,ctypes.byref(handle))!=0 and not handle.value
 return {'cases':results,'malformed_header_refused':True,'passed':True}

if __name__=='__main__':
 import sys
 print(json.dumps(exercise(ctypes.CDLL(sys.argv[1])),indent=2))
