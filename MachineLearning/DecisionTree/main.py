import preprocess
import dtree
import id3

c = preprocess.Census()


dfile = open('./traindata-file', 'r')
vfile = open('./values-file', 'r')
tfile = open('./testdata-file', 'r')

c.make_values('values-file')

data= []

test= []
attributes = c.attributes
target_attr = attributes[-1]
# Create a list of all the lines in the data file
lines = [line.strip() for line in dfile.readlines()]

# Creating a list of all lines in Test File
testlines = [line.strip() for line in tfile.readlines()]


for line in lines:
    data.append(dict(zip(attributes,
                [datum.strip() for datum in line.split(",")])))
for line in testlines:    
    test.append(dict(zip(attributes,
                [datum.strip() for datum in line.split(",")])))

print 'Calling create_decision_tree()' 
#print 'Values : ', c.values
#print 'Data : ',c.data[:100]
#print 'Attributes : ',attributes
#print 'Target-Attr : ',target_attr
print 'Number of Entries in Training Set after Cleanup', len(data)
print 'Number of Entries in Test Set after Cleanup', len(test)

d = input('No. of Training Instances to be taken: ')
s1 = input('Start from Index: ')

tree = dtree.create_decision_tree(c.values, data[s1:s1+d], attributes, target_attr, id3.gain, None)

print '-----------------Decision Tree Created------------------'
h = preprocess.Helper()

h.print_tree(tree, "")
t = input('No. of Test Instances to be taken: ')
s2 = input('Start from Index: ')
classification = dtree.classify(tree, test[s2:s2+t])
#print classification
#print test[s2:s2+t]
correct = 0
i = 0
for item in classification:
    #print item
    if test[i][target_attr] == (item+'.'):
        correct +=1
    i +=1
total = i

print '----------------Classification Results------------------'
print "Correctly-Classified: ", correct
print "Total-Classifications: ", total
print "Accuracy: ", (float(correct)/total)*100