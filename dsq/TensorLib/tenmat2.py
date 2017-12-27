#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('.'))
import numpy;
import tensor;
import tools;


class tenmat2:

    data = None;
    rindices = None;
    cindices = None;
    tsize = None;

    def __init__(self, T, rdim = None, cdim = None, tsiz = None, option = None):

        if(rdim is not None and rdim.__class__ == list):
            rdim = numpy.array(rdim);
        if(cdim is not None and cdim.__class__ == list):
            cdim = numpy.array(cdim);
        if(tsiz is not None and tsiz.__class__ == list):
            tsiz = numpy.array(tsiz);


    #constructor for the call tenmat(A, RDIMS, CDIMS, TSIZE)
        if(rdim is not None and cdim is not None and tsiz is not None):
            if(T.__class__ == numpy.ndarray):
                # self.data = T.copy();
                self.data = T
            if(T.__class__ == tensor.tensor):
                # self.data = T.data.copy();
                self.data = T.data
            self.rindices = rdim;
            self.cindices = cdim;
            # self.tsize = tuple(tsiz);
            self.tsize = tsiz

            n = len(self.tsize);

            temp = numpy.concatenate((self.rindices,self.cindices));
            temp.sort();
            if not ((numpy.arange(n) == temp).all()):
                raise ValueError("Incorrect specification of dimensions");
            elif (tools.getelts(self.tsize, self.rindices).prod()
                  != len(self.data)):
                raise ValueError("size(T,0) does not match size specified");
            elif (tools.getelts(self.tsize, self.cindices).prod()
                  != len(self.data[0])):
                raise ValueError("size(T,1) does not match size specified");

            return;



    #convert tensor to a tenmat
        if(rdim is None and cdim is None):
            self.data = None;
            self.rindices = None;
            self.cindices = None;
            self.tsize = None;
            return
        #     raise ValueError("Both of rdim and cdim are not given");

        # T = T.copy(); #copy the tensor


        self.tsize = numpy.array(T.shape);
        n = T.ndims();

        if (rdim is not None):
            if(cdim is not None):
                rdims = rdim;
                cdims = cdim;
            elif(option is not None):
                if(option == 'fc'):
                    rdims = rdim;
                    if(rdims.size != 1):
                        raise ValueError("only one row dimension for 'fc' option");

                    cdims = [];
                    for i in range(rdim[0]+1,n):
                        cdims.append(i);
                    for i in range(0, rdim[0]):
                        cdims.append(i);
                    cdims = numpy.array(cdims);


                elif(option == 'bc'):
                    rdims = rdim;
                    if(rdims.size != 1):
                        raise ValueError("only one row dimension for 'bc' option");
                    cdims = [];
                    for i in range(0, rdim[0])[::-1]:
                        cdims.append(i);
                    for i in range(rdim[0]+1,n)[::-1]:
                        cdims.append(i);
                    cdims = numpy.array(cdims);

                elif(option == 't'):
                    cdims = rdim
                    rdims = tools.notin(n, cdims)


                else:
                    raise ValueError("unknown option {0}".format(option));

            #一般只指定rdims的执行这里
            else:
                rdims = rdim;
                cdims = tools.notin(n, rdims);

        else:
            if(option == 't'):
                cdims = cdim;
                rdims = tools.notin(n, cdims);
            else:
                raise ValueError("unknown option {0}".format(option));


        #error check
        temp = numpy.concatenate((rdims,cdims));
        temp.sort();
        if not ((numpy.arange(n) == temp).all()):
            raise ValueError("error, Incorrect specification of dimensions");


        #permute T so that the dimensions specified by RDIMS come first

        #!!!! order of data in ndarray is different from that in Matlab!
        #this is (kind of odd process) needed to conform the result with Matlab!
        #lis = list(T.shape);
        #temp = lis[T.ndims()-1];
        #lis[T.ndims()-1] = lis[T.ndims()-2];
        #lis[T.ndims()-2] = temp;
        #T.data = T.data.reshape(lis).swapaxes(T.ndims()-1, T.ndims()-2);
        #print T;


        #T = T.permute([T.ndims()-1, T.ndims()-2]+(range(0,T.ndims()-2)));
        #print T;

        # ------原始是permute------------
        # T = T.permute(numpy.concatenate((rdims,cdims)));


        #convert T to a matrix;

        # -------这里我改成了without_copy

        T = T.permute_without_copy(numpy.concatenate((rdims,cdims)));


        row = tools.getelts(self.tsize, rdims).prod()
        col = tools.getelts(self.tsize, cdims).prod()

        self.data = T.data.reshape([row, col]);
        self.rindices = rdims;
        self.cindices = cdims;


    def copy(self):
        return tenmat2(self.data, self.rindices, self.cindices, self.tsize) ;



    def totensor(self):
        sz = self.tsize;
        order = numpy.concatenate((self.rindices, self.cindices));
        order = order.tolist();
        data = self.data.reshape(tools.getelts(sz,order));

        data = tensor.tensor(data).ipermute(order).data;

        return tensor.tensor(data, sz);

    def tondarray(self):
        """returns an ndarray(2-D) that contains the same value with the tenmat"""
        return self.data;

    def mtimes(self, B):
        tsize = numpy.hstack((self.tsize[self.rindices], B.tsize[B.cindices]))
        data = tensor.tensor([])
        C = tenmat2(data)
        C.rindices = numpy.array(range(0, len(self.rindices)))
        C.cindices = numpy.array(range(0, len(B.cindices))) + len(self.rindices)
        C.data = numpy.dot(self.data, B.data)
        C.tsize = tsize
        return C

    def __str__(self):
        ret = "";
        ret += "matrix corresponding to a tensor of size {0}\n".format(self.tsize);
        ret += "rindices {0}\n".format(self.rindices);
        ret += "cindices {0}\n".format(self.cindices);
        ret += "{0}\n".format(self.data);
        return ret;
