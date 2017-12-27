#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('.'))
import numpy
import sptensor
import tools
import tenmat
import tenmat2

class tensor:
    
    data = None;
    shape = None;
    
    def __init__(self, data, shape = None):
        """Constructor for tensor object.
        dat can be numpy.array or list.
        shape can be numpy.array, list, tuple of integers"""
        if(data.__class__ == list):
            data = numpy.array(data);

        if(shape is not None):
            if(len(shape) == 0):
                raise ValueError("Second argument must be a row vector.");
            
            if(shape.__class__ == numpy.ndarray):
                if(shape.ndim != 2 and shape[0].size != 1):
                    raise ValueError("Second argument must be a row vector.");
            shape = tuple(shape);
        else:
            shape = tuple(data.shape);
        

        if (len(shape) == 0):
            if (data.size != 0):
                raise ValueError("Empty tensor cannot contain any elements");
        
        elif (tools.prod(shape) != data.size):
            raise ValueError("Size of data does not match specified size of tensor");
            
        self.shape = shape;
        # self.data = data.reshape(self.shape).copy();
        self.data = data.reshape(self.shape);

    
    def size(self):
        """returns the number of elements in the tensor"""
        ret = 1;
        for i in range(0, len(self.shape)):
            ret = ret * self.shape(i);
        return ret;
    
    def __str__(self):
        str = "tensor of size {0}\n".format(self.shape);
        str += self.data.__str__();
        return str;

    def copy(self):
        """ returns the deepcopy of tensor object."""
        return tensor(self.data.copy(), self.shape);

    def dimsize(self, ind):
        """ returns the size of the specified dimension.
        Same as shape[ind]."""
        return self.shape[ind];
    
    def ndims(self):
        """ returns the number of dimensions. """
        return len(self.shape);

    def tosptensor(self):
        """ returns the sptensor object
        that contains the same value with the tensor object."""
        
        length = len(self.shape);
        
        sub = tools.allIndices(self.shape);
        return sptensor.sptensor(
            sub,
            self.data.flatten().reshape(self.data.size, 1),
            self.shape);    
    
    def permute(self, order):
        """ returns a tensor permuted by the order specified. """
        # 其实感觉难道不是和ndarray的transpose是一样的吗,应该不需要再重写吧?
        if (order.__class__ == list):
            order = numpy.array(order);
            
        if(self.ndims() != len(order)):
            raise ValueError("Invalid permutation order");
           
        sortedorder = order.copy();
        sortedorder.sort();
        
        if not ((sortedorder == numpy.arange(self.data.ndim)).all()):
            raise ValueError("Invalid permutation order");
        
        neworder = numpy.arange(len(order)).tolist();
        newshape = list(self.shape);
        newdata = self.data.copy();

        # ------原始有copy 这里改成没copy看看
        # newdata = self.data



        for i in range(0,len(order)-1):
            index = tools.find(neworder, order[i]);
            newdata = newdata.swapaxes(i,index);

            #shape中的对应维数交换
            temp = newshape[i];
            newshape[i] = newshape[index];
            newshape[index] = temp;

            #这里是在整理neworder中的元素,扫过的元素变成和order中一样,后面的接着查找
            temp = neworder[i];
            neworder[i] = neworder[index];
            neworder[index] = temp;
        
        newshape = tuple(newshape);
        return tensor(newdata,newshape);


    def permute_without_copy(self, order):
        """ returns a tensor permuted by the order specified. """
        # 其实感觉难道不是和ndarray的transpose是一样的吗,应该不需要再重写吧?
        if (order.__class__ == list):
            order = numpy.array(order);

        if(self.ndims() != len(order)):
            raise ValueError("Invalid permutation order");

        sortedorder = order.copy();
        sortedorder.sort();

        if not ((sortedorder == numpy.arange(self.data.ndim)).all()):
            raise ValueError("Invalid permutation order");

        neworder = numpy.arange(len(order)).tolist();
        newshape = list(self.shape);
        # newdata = self.data.copy();

        # ------原始有copy 这里改成没copy看看
        newdata = self.data



        for i in range(0,len(order)-1):
            index = tools.find(neworder, order[i]);
            newdata = newdata.swapaxes(i,index);

            #shape中的对应维数交换
            temp = newshape[i];
            newshape[i] = newshape[index];
            newshape[index] = temp;

            #这里是在整理neworder中的元素,扫过的元素变成和order中一样,后面的接着查找
            temp = neworder[i];
            neworder[i] = neworder[index];
            neworder[index] = temp;

        newshape = tuple(newshape);
        return tensor(newdata,newshape);


    
    def ipermute(self, order):
        """ returns a tensor permuted by the inverse of theorder specified. """
        
        #calculate the inverse of iorder
        iorder = [];
        for i in range(0, len(order)):
            iorder.extend([tools.find(order, i)]);
        
        #returns the permuted tensor by the inverse
        return self.permute(iorder);
        

    def ttm(self, mat, dims = None, option = None):
        """ computes the tensor times the given matrix.
        arrs is a single 2-D matrix/array or a list of those matrices/arrays."""
        
        if(dims == None):
            dims = range(0,self.ndims());
        
        #Handle when arrs is a list of arrays
        if(mat.__class__ == list):
            if(len(mat) == 0):
                raise ValueError("the given list of arrays is empty!");
            
            (dims,vidx) = tools.tt_dimscehck(dims, self.ndims(), len(mat));
            
            Y = self.ttm(mat[vidx[0]],dims[0],option);
            for i in range(1, len(dims)):
                Y = Y.ttm(mat[vidx[i]],dims[i],option);
                
            return Y;                
        
        if(mat.ndim != 2):
            raise ValueError ("matrix in 2nd armuent must be a matrix!");
        
        if(dims.__class__ == list):
            if(len(dims) != 1):
                raise ValueError("Error in number of elements in dims");
            else:
                dims = dims[0];
        
        if(dims < 0 or dims > self.ndims()):
            raise ValueError ("Dimension N must be between 1 and num of dimensions");
        
        
        #Compute the product
        
        N = self.ndims();
        shp = self.shape;
        order = []
        order.extend([dims]);
        order.extend(range(0,dims));
        order.extend(range(dims+1,N));

        # 第一步把对应模I Permute到第一个,然后reshape成(I,I~)
        # 第二步matrix * 上面得到的矩阵
        
        newdata = self.permute(order).data;
        newdata = newdata.reshape(shp[dims], tools.prod(shp)/shp[dims]);
        if(option == None):
            newdata = numpy.dot(mat, newdata);
            p = mat.shape[0];
        elif(option == 't'):
            newdata = numpy.dot(mat.transpose(), newdata);
            p = mat.shape[1];
        else:
            raise ValueError("Unknown option");
        
        newshp = [p];
        newshp.extend(tools.getelts(shp,range(0,dims)));
        newshp.extend(tools.getelts(shp,range(dims+1,N)));
        
        Y = tensor(newdata, newshp);
        # 这里的ipermute很关键,按照相反permute,理解的不是很直观,有时间可以多想想
        Y = Y.ipermute(order);
        return Y;


    def ttv(self, vec, dims = None):
        if(dims is None):
            dims = range(0, self.ndims())

        if(vec.__class__ == list):
            if(len(vec) == 0):
                raise ValueError("the given list of arrays is empty!")

                (dims, vidx) = tools.tt_dimscheck(dims, self.ndims(), len(vec))
                Y = self.ttv(vec[vidx[0]], dims[0])
                for i in range(1, len(dims)):
                    Y = Y.ttv(vec[videx[i]], dims[i])

                return Y
        if(vec.ndim != 1):
            raise ValueError("param in 2nd argment must be a vector")

        if(dims.__class__ == list):
            if(len(dims) != 1):
                raise ValueError("Error in number of elements in dims");
            else:
                dims = dims[0]

        if(dims < 0 or dims > self.ndims()):
            raise ValueError ("Dimension N must be between 1 and num of dimensions");

        N = self.ndims()
        shp = self.shape
        order = []
        order.extend(range(0,dims))
        order.extend(range(dims+1,N))
        order.extend([dims])

        newdata = self.permute(order).data
        newdata = newdata.reshape(tools.prod(shp)/shp[dims], shp[dims]);

        newdata = numpy.dot(newdata, vec)
        N -= 1

        sz = numpy.array(self.shape)[order]
        newshp = sz[:N]

        # newshp = []
        # newshp.extend(tools.getelts(shp, range(0, dims)))
        # newshp.extend(tools.getelts(shp, range(dims+1, N)))

        Y = tensor(newdata, newshp)
        return Y


    def ttt(self, tB, adims, bdims):
        amatrix = tenmat.tenmat(self, adims, option='t')
        bmatrix = tenmat.tenmat(tB, bdims)
        cmatrix = amatrix.mtimes(bmatrix)

        c = cmatrix.totensor()
        return c


    def ttt_without_copy(self, tB, adims, bdims):
        amatrix = tenmat2.tenmat2(self, adims, option='t')
        bmatrix = tenmat2.tenmat2(tB, bdims)
        cmatrix = amatrix.mtimes(bmatrix)

        c = cmatrix.totensor()
        return c


    def einstain_ttt_without_copy(self,tB,adims,bdims):

        B = tB.copy()
        B = B.tondarray()
        shape = B.shape
        shape = shape + (1,)
        B = B.reshape(shape)
        B = tensor(B)

        c = self.ttt_without_copy(B, adims, bdims)
        c = c.tondarray()
        c = numpy.squeeze(c)
        c = tensor(c)
        return c


    # 所有模都乘光了
    def einstein_ttt(self, tB, adims, bdims):
        B = tB.copy()
        B = B.tondarray()
        shape = B.shape
        shape = shape + (1,)
        B = B.reshape(shape)
        B = tensor(B)

        c = self.ttt(B, adims, bdims)
        c = c.tondarray()
        c = numpy.squeeze(c)
        c = tensor(c)
        return c


    
    def tondarray(self):
        """return an ndarray that contains the data of the tensor"""
        return self.data;
    


# Math, logic operators

    def __add__(self, other):
        return self.funwrap(other, "add");
    def __sub__(self, other):
        return self.funwrap(other, "sub");
    def __mul__(self, other):
        return self.funwrap(other, "mul");
    def __eq__(self, other):
        return self.funwrap(other, "eq");
    def __ne__(self, other):
        return self.funwrap(other, "ne");
    def __lt__(self, other):
        return self.funwrap(other, "lt");
    def __gt__(self, other):
        return self.funwrap(other, "gt");
    def __le__(self, other):
        return self.funwrap(other, "le");
    def __ge__(self, other):
        return self.funwrap(other, "ge");
    def funwrap(self, other, fun):
        """rwaper function for logical operators"""
        if(other.__class__ == tensor):
            if(self.shape != other.shape):
                raise ValueError("Shapes of the tensors do not match");
            
            if(fun == "add"):
                return tensor(self.data.__add__(other.data), self.shape);
            elif(fun == "sub"):
                return tensor(self.data.__sub__(other.data), self.shape);
            elif(fun == "mul"):
                raise ValueError("Use ttt() instead.");
            elif(fun == "eq"):
                return tensor(self.data.__eq__(other.data), self.shape);
            elif(fun == "ne"):
                return tensor(self.data.__ne__(other.data), self.shape);
            elif(fun == "gt"):
                return tensor(self.data.__gt__(other.data), self.shape);
            elif(fun == "ge"):
                return tensor(self.data.__ge__(other.data), self.shape);
            elif(fun == "lt"):
                return tensor(self.data.__lt__(other.data), self.shape);
            elif(fun == "le"):
                return tensor(self.data.__le__(other.data), self.shape);
            else:
                raise ValueError("Unknown function");
        else:
            if(fun == "add"):
                return tensor(self.data.__add__(other), self.shape);
            elif(fun == "sub"):
                return tensor(self.data.__sub__(other), self.shape);
            elif(fun == "mul"):
                return tensor(self.data.__mul__(other), self.shape);
            elif(fun == "eq"):
                return tensor(self.data.__eq__(other), self.shape);
            elif(fun == "ne"):
                return tensor(self.data.__ne__(other), self.shape);
            elif(fun == "gt"):
                return tensor(self.data.__gt__(other), self.shape);
            elif(fun == "ge"):
                return tensor(self.data.__ge__(other), self.shape);
            elif(fun == "lt"):
                return tensor(self.data.__lt__(other), self.shape);
            elif(fun == "le"):
                return tensor(self.data.__le__(other), self.shape);
            else:
                raise ValueError("Unknown function");

    def __pos__(self):
        pass; #do nothing
    def __neg__(self):
        return tensor(self.data * -1, self.shape);
        
        
    #Special Constructors
def tenzeros(shp):
    """special constructor, construct a tensor with the shape filled with 0"""
    data = numpy.ndarray(shp);
    data.fill(0);
    return tensor(data, shp);
def tenones(shp):
    """special constructor, construct a tensor with the shape filled with 1"""
    data = numpy.ndarray(shp);
    data.fill(1);
    return tensor(data, shp);
def tenrands(shp):
    """special constructor, construct a tensor with the shape filled with random number between 0 and 1"""
    data = numpy.random.random(shp);
    return tensor(data, shp);
def tendiag(vals, shape=None):
    """special constructor, construc a tensor with the values in the diagonal"""
    
    #if shape is None or
    #number of dimensions of shape is less than the number of values given
    if (shape == None or len(shape) < len(vals)):
        shape = [len(vals)]*len(vals);
    else:
        shape = list(shape);
        for i in range(0, len(vals)):
            if(shape[i] < len(vals)):
                shape[i] = len(vals);
    
    data = numpy.ndarray(shape);
    data.fill(0);
    
    # put the values in the ndarray
    for i in range(0, len(vals)):
        data.put(tools.sub2ind(shape,[i]*len(shape)), vals[i]);
    return tensor(data, shape);    
    