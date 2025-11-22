import socket, struct, threading, os
MEM_FILE="ram.img"; SIZE=32*1024**3; PROTO_Z=b'\xAA'; PROTO_D=b'\xBB'
if not os.path.exists(MEM_FILE): open(MEM_FILE,"wb").seek(SIZE-1); open(MEM_FILE,"wb").write(b'\0')
def h(c):
 c.setsockopt(6,1,1); c.setsockopt(1,7,2*1024**2); f=open(MEM_FILE,"r+b")
 try:
  while 1:
   d=c.recv(8); 
   if not d:break
   pos=struct.unpack('>Q',d)[0]; f.seek(pos); chk=f.read(4096*32)
   for i in range(32): c.sendall(PROTO_Z if chk[i*4096:(i+1)*4096]==b'\x00'*4096 else PROTO_D+chk[i*4096:(i+1)*4096])
 except:pass
s=socket.socket(); s.bind(('0.0.0.0',9999)); s.listen(100)
while 1: c,a=s.accept(); threading.Thread(target=h,args=(c,)).start()
