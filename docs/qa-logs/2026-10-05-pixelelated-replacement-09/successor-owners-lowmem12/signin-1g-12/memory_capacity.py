def accepts(args,physical_kib,usable_kib):
    return (args.count('-m')==1 and args[args.index('-m')+1]=='1024'
            and physical_kib==1024*1024 and 0<usable_kib<physical_kib)
