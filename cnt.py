import struct
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

with open("01_01_201806180000_5_SUiRU/2018061800000101VM.cnt","rb") as f:
    format_id,format_version,reserved=struct.unpack(">BBH",f.read(1+1+2))
    print(format_id,format_version,reserved)

    start_date,frame_timespan,datablock_length=struct.unpack(">QII",f.read(8+4+4))

    print(hex(start_date),frame_timespan,datablock_length)

    while True:
        try:
            organization_id,organization_net_id,channel_id,sample_size_and_number,first_data=struct.unpack(">BBHHi",f.read(1+1+2+2+4))
            #任意ビット数で入力出来る?
            sample_size=(sample_size_and_number>>12) & 0xF
            sample_number=sample_size_and_number & 0xFFF
            print(organization_id,organization_net_id,channel_id,sample_size,sample_number,first_data)
            if sample_size!=1:
                print("だめ．差分が1Byteじゃない",sample_size)
            data=[first_data]
            for i in range(sample_number-1):
                data.append(data[i]+int(struct.unpack(">b",f.read(1))[0]))
            plt.plot(data)
        except Exception:
            pass
    plt.show()
