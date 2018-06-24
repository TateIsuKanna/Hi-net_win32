import struct
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import pathlib

total_data=[]
for path in pathlib.Path("data").glob("*.cnt"):
    with open(path,"rb") as f:
        format_id,format_version,reserved=struct.unpack(">BBH",f.read(1+1+2))
        print(format_id,format_version,reserved)

        while True:
            header_bytesarray=f.read(8+4+4)
            if not header_bytesarray:
                break
            start_date,frame_timespan,datablock_length=struct.unpack(">QII",header_bytesarray)
            print(hex(start_date),frame_timespan,datablock_length)
            datablock_pointer=0
            while True:
                organization_id,organization_net_id,channel_id,sample_size_and_number,first_data=struct.unpack(">BBHHi",f.read(1+1+2+2+4))
                datablock_pointer+=1+1+2+2+4
                sample_size=(sample_size_and_number>>12) & 0xF
                sample_number=sample_size_and_number & 0xFFF
                #print(sample_size,sample_number)
                #print(organization_id,organization_net_id,hex(channel_id),first_data)
                if channel_id==0x55f3:
                    total_data.append(first_data)
                past_data=first_data
                if sample_size==0:
                    #TODO:
                    print("sample_size is zero")
                    for i in range(math.ceil((sample_number-1)/2)):
                        current_data=int(struct.unpack("b",f.read(1))[0])
                        datablock_pointer+=1
                else:
                    if channel_id==0x55f3:
                        for i in range(sample_number-1):
                            if sample_size==3:
                                current_data=int.from_bytes(f.read(3),'big', signed=True)
                                datablock_pointer+=3
                            else:
                                current_data=int(struct.unpack(">"+[" ","b","h"," ","i"][sample_size],f.read(sample_size))[0])
                                datablock_pointer+=sample_size
                                total_data.append(past_data+current_data)
                            past_data=past_data+current_data
                    else:
                        f.read(sample_size*(sample_number-1))
                        datablock_pointer+=sample_size*(sample_number-1)
                if datablock_pointer==datablock_length:
                    break
total_data=total_data-np.average(total_data[:100000])
plt.plot(total_data,linewidth=.5)
plt.plot(np.cumsum(total_data),linewidth=.5)
#plt.plot(np.diff(total_data),linewidth=.5)
#plt.plot(np.log(np.sqrt(np.array(total_data)**2)),linewidth=.5)
plt.show()
