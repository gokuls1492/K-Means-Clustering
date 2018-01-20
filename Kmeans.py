from __future__ import division
import pandas as pd
import math
import copy
import sys

#Authors : Gokul & Padma

def euclidean_distance(point_1, point_2):
    distance = math.pow(point_1[1]['x'] - point_2[1]['x'],2) + math.pow(point_1[1]['y'] - point_2[1]['y'],2)
    return math.sqrt(distance)

def perform_clustering(k, data_frame, max_iter, toler):
    centroid  = copy.deepcopy(data_frame.iloc[0:k])
    flag = False
    classes = dict()
    for i in range(max_iter):
        classes.clear()
        for j in range(k):
            classes[j] = list()
        for entry in data_frame.iterrows():
            distances = [euclidean_distance(entry, cent) for cent in centroid.iterrows()]
            class_index = distances.index(min(distances))
            classes[class_index].append(entry)

        prev = copy.deepcopy(centroid)

        for index in classes:
            x_value =0; y_value=0
            for item in range(len(classes[index])):
                x_value += classes[index][item][1]['x']
                y_value += classes[index][item][1]['y']
            x_avg = round(x_value/len(classes[index]),2)
            y_avg = round(y_value/len(classes[index]),2)
            centroid.set_value(index,'x',x_avg)
            centroid.set_value(index, 'y', y_avg)

        for cent_index, rows in centroid.iterrows():
            new_val = rows
            old_val = prev.iloc[cent_index]
            diff = (new_val['x'] == old_val['x']) and (new_val['y'] == old_val['y'])
            if diff:
                flag=True
            else:
                flag=False
        if flag:
            break
    return classes, centroid

def get_distance(entry, class_index, centroid, index):
    dist = math.pow(entry[class_index][1]['x']-centroid.iloc[index]['x'],2) + math.pow(entry[class_index][1]['y']-centroid.iloc[index]['y'],2)
    return math.sqrt(dist)

def evaluate_sse(data, centroid):
    sse=0
    for index, entry in data.iteritems():
        for classes in range(len(entry)):
            sse+= math.pow(get_distance(entry,classes,centroid,index), 2)
    return sse


def main():
    k_value = int(sys.argv[1])
    file_path = sys.argv[2]
    output_path = sys.argv[3]
    max_iterations = 25
    tolerance_val = 0.01
    data_frame = pd.read_csv(file_path, delimiter='\t')
    output, centroid = perform_clustering(k_value, data_frame.iloc[:,1:], max_iterations, tolerance_val)
    sse = evaluate_sse(output, centroid)

    output_file = open(output_path,'w')
    for index, val in output.iteritems():
        temp =[]
        for items in val:
            temp.append(items[0])
        output_file.write(str(index)+"\t"+(str(temp))+"\n")
    output_file.write("SSE: "+str(sse))
    output_file.close()
    print sse

if __name__ == '__main__':
    main()