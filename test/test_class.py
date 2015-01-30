import test_class0
import test_class1

#bb= B()
#cc= B()
#A.aaa= '789'
if(1):

            
        cls = getattr(test_class1, 'B', None) 
        #print obj
        obj = cls()
        func = getattr(obj, 'bbb', None)
    
        #print func
        func()

        cls = getattr(test_class1, 'B', None) 
        obj2 = cls()
        func2 = getattr(obj2, 'bbb', None)
    
       
        func2()	        