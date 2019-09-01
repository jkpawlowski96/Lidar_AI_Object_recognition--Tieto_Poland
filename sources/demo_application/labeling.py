from preprocessing.dataset import datascore
from lidar_readings.find import find_paths



files1 = ['../lidar_readings/m1_1cm.txt',
          '../lidar_readings/m1_5cm.txt',
          '../lidar_readings/m2_1cm.txt',
          '../lidar_readings/m2_5cm.txt',
          '../lidar_readings/m3_1cm.txt',
          '../lidar_readings/m3_5cm.txt']

files2 = ['../lidar_readings/s1.txt',
          '../lidar_readings/s2.txt',
          '../lidar_readings/s3.txt',
          '../lidar_readings/s4.txt',
          '../lidar_readings/s5.txt',
          '../lidar_readings/s6.txt',
          '../lidar_readings/s7.txt',
          '../lidar_readings/s8.txt',
          '../lidar_readings/s9.txt',
          '../lidar_readings/s10.txt',
          '../lidar_readings/s11.txt',
          '../lidar_readings/s12.txt']
files3 =[ '../lidar_readings/t2.txt',
          '../lidar_readings/t3.txt',
          '../lidar_readings/t4.txt',
          '../lidar_readings/t5.txt',
          '../lidar_readings/t6.txt',
          '../lidar_readings/t7.txt',
          '../lidar_readings/t9.txt',
          '../lidar_readings/t10.txt',
          '../lidar_readings/t11.txt',
          '../lidar_readings/t12.txt']

files4 = find_paths('n.txt')

for f in files4:
    print(f)
    datascore(f, prep=True)


