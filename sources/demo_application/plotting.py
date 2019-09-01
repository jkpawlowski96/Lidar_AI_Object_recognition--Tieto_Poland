from ploting.lidar_plot import plot_file

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

files3=['../lidar_readings/n1.txt']

# preprocessing properties
max_to_interpolate = 5
g = 0.5


def main():
        plot_file(filename=files2[0])
        plot_file(filename=files2[0], gauss=g)
        plot_file(filename=files2[0], interpolation=max_to_interpolate)
        plot_file(filename=files2[0], gauss=g, interpolation=max_to_interpolate)


if __name__ == "__main__":
    main()

