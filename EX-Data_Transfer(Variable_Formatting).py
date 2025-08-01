
fmt = '!cBcB' + 'I' * (1 + len(coin_ts) + 1) #Variable packet formating

combined_data = [inst, ch, RF, ID, bh_ts] + coin_ts + [event_num] #Assuming coin_ts is a list of variable length

ustruct.pack(fmt, *combined_data)

#Note:
    #To use this method an additional byte will need to be sent with the packet to specify the length of the coin_ts length