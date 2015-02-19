'''class RRCU:
    def __init__(self,a=None):

        self.rows_ptrs=[]
        self.cols_nums=[]
        self.elements=[]
        k=0;
        if a:
            for i in range(0,len(a)):
                for j in range(0,len(a[i])):
                    if a[i][j]:
                        k+=1
                        self.elements.append(a[i][j])
                        self.cols_nums.append(j+1);
                        if len(self.rows_ptrs)<=i:
                            self.rows_ptrs.append(k);
                if len(self.rows_ptrs)<=i:
                    self.rows_ptrs.append(k+1);
            self.rows_ptrs.append(k+1);
'''
'''def restore_matrix(sparse,n,m):
    a=[[0.0 for j in range(0,m)] for i in range(0,n)]
    row=0;
    for i in range(0,len(sparse.rows_ptrs)-1):
        for j in range(sparse.rows_ptrs[i]-1,sparse.rows_ptrs[i+1]-1):
            a[i][sparse.cols_nums[j]-1]=sparse.elements[j];
    
    return a
'''
'''
def sum_rrcu(rrcu1,rrcu2):
    res=None
    if rrcu1 and rrcu2:
        res=RRCU() ; l=0;
        for i in range(0,len(rrcu1.rows_ptrs)-1):
            used=[]
            line_a=rrcu1.cols_nums[rrcu1.rows_ptrs[i]-1:rrcu1.rows_ptrs[i+1]-1]
            line_b=rrcu2.cols_nums[rrcu2.rows_ptrs[i]-1:rrcu2.rows_ptrs[i+1]-1]
            for j in line_a:
                if j in line_b:
                    ind_j=line_a.index(j)+rrcu1.rows_ptrs[i]-1;
                    ind_k=line_b.index(j)+rrcu2.rows_ptrs[i]-1;
                    if rrcu1.elements[ind_j]!=-rrcu2.elements[ind_k]:
                        l+=1
                        res.elements.append(rrcu1.elements[ind_j]+rrcu2.elements[ind_k]);
                        res.cols_nums.append(j)
                        if len(res.rows_ptrs)<=i:
                            res.rows_ptrs.append(l);
                    used.append(j)
                else:
                    l+=1
                    ind_j=line_a.index(j)+rrcu1.rows_ptrs[i]-1;
                    res.elements.append(rrcu1.elements[ind_j]);
                    res.cols_nums.append(j)
                    if len(res.rows_ptrs)<=i:
                        res.rows_ptrs.append(l);
            for j in  line_b:
                if not (j in used):
                    l+=1
                    ind_k=line_b.index(j)+rrcu2.rows_ptrs[i]-1
                    res.elements.append(rrcu2.elements[ind_k]);
                    res.cols_nums.append(j)
                    if len(res.rows_ptrs)<=i:
                        res.rows_ptrs.append(l);
            if len(res.rows_ptrs)<=i:
                    res.rows_ptrs.append(l+1);
        res.rows_ptrs.append(l+1);
    return res        
'''
'''def sum_sparse(sp1,sp2):
    res=None
    if sp1 and sp2:
        res=RRCU() ; l=0;
        for i in range(0,len(sp1.rows_ptrs)-1):
            print("i=",i)
            j=sp1.rows_ptrs[i]-1;k=sp2.rows_ptrs[i]-1;
            while (j <sp1.rows_ptrs[i+1]-1 and
                    k <sp2.rows_ptrs[i+1]-1):
                ind_j=sp1.cols_nums[j];ind_k=sp2.cols_nums[k];
                if ind_j==ind_k:
                    print("ind_j==ind_k is entered")
                    if sp1.elements[j]!=-sp2.elements[k]:
                        l+=1
                        res.elements.append(sp1.elements[j]+sp2.elements[k]);
                        res.cols_nums.append(ind_j)
                        if len(res.rows_ptrs)<=i:
                            res.rows_ptrs.append(l);
                    j+=1;k+=1;
                elif ind_k<ind_j:
                    print("k<j is entered")
                    l+=1
                    res.elements.append(sp2.elements[k]);
                    res.cols_nums.append(ind_k)
                    if len(res.rows_ptrs)<=i:
                        res.rows_ptrs.append(l);
                    k+=1
                else:
                    print("k>j is entered")
                    l+=1
                    res.elements.append(sp1.elements[j]);
                    res.cols_nums.append(ind_j)
                    if len(res.rows_ptrs)<=i:
                        res.rows_ptrs.append(l);
                    j+=1
            while j <sp1.rows_ptrs[i+1]-1:
                ind_j=sp1.cols_nums[j];
                l+=1
                res.elements.append(sp1.elements[j]);
                res.cols_nums.append(ind_j)
                if len(res.rows_ptrs)<=i:
                    res.rows_ptrs.append(l);
                j+=1
            while k <sp2.rows_ptrs[i+1]-1:
                ind_k=sp2.cols_nums[k];
                l+=1
                res.elements.append(sp2.elements[k]);
                res.cols_nums.append(ind_k)
                if len(res.rows_ptrs)<=i:
                    res.rows_ptrs.append(l);
                k+=1
            if len(res.rows_ptrs)<=i:
                    res.rows_ptrs.append(l+1);
        res.rows_ptrs.append(l+1);
    return res
'''
