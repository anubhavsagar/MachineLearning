class Census:
    def __init__(self):
        pass

    attributes = ['age', 'workclass', 'fnlwgt', 
                  'education', 'education-num', 
                  'marital-status', 'occupation', 
                  'relationship', 'race', 'sex', 
                  'capital-gain', 'capital-loss', 
                  'hours-per-week', 'native-country',
                  'class']
    
    target_attr = 'class'
    
    values = {}
    
    data = []
    
    test = []
    
    def make_values(self, filename):
        file1 = open(filename)
        for line in file1:
            l = line.split(':')
            self.values[l[0]] = l[1].strip().replace(' ', '').split(',')
        print 'Possible Values stored in a Dictionary'
        
    def make_data(self, filename):
        file2 = open(filename)
        for line in file2:
            self.data.append(line.strip().replace(' ', '').split(','))
        self.data =  self.data[:-1]
        print 'Data stored in a list'
        print 'Number of Entries in Data Set: ' + str(len(self.data))
    
    def make_test_data(self, filename):
        f = open(filename)
        for line in f:
            self.test.append(line[:-1].strip().replace(' ', '').split(','))
        self.test =  self.test[:-1]
        print 'Test Data stored in a list'
        print 'Number of Entries in Test Set: ' + str(len(self.test))
    
    continuous_attr = ['age', 'fnlwgt', 'education-num', 
                       'capital-gain', 'capital-loss', 'hours-per-week']
    
    def remove_unknows(self):
        newdata = []
        newtest = []
        for record in self.data:
            flag = False
            for attr in self.attributes:
                if record[self.attributes.index(attr)] == '?':
                    flag = True
            if flag == False:
                newdata.append(record)
        for record in self.test:
            flag = False
            for attr in self.attributes:
                if record[self.attributes.index(attr)] == '?':
                    flag = True
            if flag == False:
                newtest.append(record)
        self.data = newdata
        self.test = newtest
           
    def modify_data(self):
        h = Helper()
        for attr in self.continuous_attr:
            self.values[attr] = h.get_values(attr)
            i = self.attributes.index(attr)
            for record in self.data:
                val = record[i]
                record[i] = h.get_category(val,attr)
            for record in self.test:
                val = record[i]
                record[i] = h.get_category(val,attr)
    
    def export_data(self, dfile, vfile, tfile):
        h = Helper()
        #h.print_list(self.attributes, dfile)

        for record in self.data:
            h.print_list(record, dfile)
            dfile.write('\n')
            
        for key, value in self.values.iteritems():
            vfile.write(key+': ')
            h.print_list(value, vfile)
            vfile.write('\n')
        
        #h.print_list(self.attributes, tfile)
        for record in self.test:
            h.print_list(record, tfile)
            tfile.write('\n')
    
    def replace_unknowns(self):
        majority = {}
        for attr in self.attributes:
            maj = []
            for entry in self.values[attr]:
                maj.append(0)
    
            for record in self.data:
                if record[self.attributes.index(attr)] == '?':
                    continue
                else:
                    maj[self.values[attr].index(record[self.attributes.index(attr)])] +=1
            
            max = 0
            i = 0
            for entry in self.values[attr]:
                if entry > max:
                    maxindex = i
                    max = entry
                else:
                    i +=1
            majority[attr] = self.values[attr][maxindex]
        
        for record in self.data:
            for attr in self.attributes:
                if record[self.attributes.index(attr)]=='?':
                    record[self.attributes.index(attr)] = majority[attr]
        for record in self.test:
            for attr in self.attributes:
                if record[self.attributes.index(attr)]=='?':
                    record[self.attributes.index(attr)] = majority[attr]
        
#HELPER FUNCTIONS
#---------------------------------------------------------------------#
class Helper:
    f = open('./dec-tree', 'w+')
    
    def print_tree(self,tree, str):
        """
        This function recursively crawls through the d-tree and prints it out in a
        more readable format than a straight print of the Python dict object.  
        """
        
        if type(tree) == dict:
            self.f.write( "%s%s\n" % (str, tree.keys()[0]))
            for item in tree.values()[0].keys():
                self.f.write( "%s\t%s\n" % (str, item))
                self.print_tree(tree.values()[0][item], str + "\t")
        else:
            self.f.write( "%s\t->\t%s\n" % (str, tree))


    def print_list(self, plist, filename):
            for val in plist[:-1]:
                filename.write(val+', ')
            filename.write(plist[-1])
                    
    def get_cat_age(self,val):
        if val < 20:
            return '10s'
        elif val < 30:
            return '20s'
        elif val < 40:
            return '30s'
        elif val < 50:
            return '40s'
        elif val < 60:
            return '50s'
        else:
            return 'old'
    def get_cat_cg(self,val):
        if val==0:
            return 'No-Gain'
        elif val<2000:
            return 'Small-Gain'
        elif val<20000:
            return 'Gain'
        else:
            return 'Huge-Gain'
    def get_cat_cl(self,val):
        if val==0:
            return 'No-Loss'
        elif val<1000:
            return 'Small-Loss'
        elif val<2500:
            return 'Loss'
        else:
            return 'Huge-Loss'
    def get_cat_hpw(self,val):
        if val < 20:
            return 'Less-Work'
        elif val < 50:
            return 'Normal-Work'
        elif val < 70:
            return 'Overtime'
        else:
            return 'Too-Much-Work'
    def get_cat_fnlwgt(self,val):
        if val < 250000:
            return 'low'
        else:
            return 'high'
    def get_cat_en(self,val):
        if val < 5:
            return '<5'
        elif val < 10:
            return '<10'
        else:
            return '>10'
    
    def get_category(self,val, attr):
        if attr == 'age':
            return self.get_cat_age(int(val))
        elif attr == 'capital-gain':
            return self.get_cat_cg(int(val))
        elif attr == 'capital-loss':
            return self.get_cat_cl(int(val))
        elif attr == 'hours-per-week':
            return self.get_cat_hpw(int(val))
        elif attr == 'fnlwgt':
            return self.get_cat_fnlwgt(int(val))
        elif attr == 'education-num':
            return self.get_cat_en(int(val))
        
    def get_values(self,attr):
        if attr == 'age':
            return ['10s','20s','30s','40s','50s','old']
        elif attr =='capital-gain':
            return ['No-Gain','Small-Gain','Gain','Huge-Gain']
        elif attr =='capital-loss':
            return ['No-Loss','Small-Loss','Loss','Huge-Loss']
        elif attr =='hours-per-week':
            return ['Less-Work','Normal-Work', 'Overtime', 'Too-Much-Work']
        elif attr == 'fnlwgt':
            return ['low', 'high']
        elif attr == 'education-num':
            return ['<5', '<10', '>10']
#----------------------------------------------------------------------#
if __name__ == '__main__':
    c = Census()
    c.make_data('data/census-income.data.txt')
    c.make_test_data('data/census-income.test.txt')
    c.make_values('data/census-income.names1.txt')
    c.modify_data()
    
    #print 'Value after Modification: ', c.values
    #print 'Data after Modification: ', c.data[:100]
    c.replace_unknowns()
    c.remove_unknows()
    
    print 'Number of Entries in Training Set after Cleanup', len(c.data)
    print 'Number of Entries in Test Set after Cleanup', len(c.test)
    
    dfile = open('./traindata-file', 'w+')
    vfile = open('./values-file', 'w+')
    tfile = open('./testdata-file', 'w+')
    
    print 'Exporting Data and Values to Files'
    c.export_data(dfile, vfile, tfile)
    
    dfile.close()
    vfile.close()
    tfile.close()
    
    print '---------------------PreProcessing Complete------------------------'