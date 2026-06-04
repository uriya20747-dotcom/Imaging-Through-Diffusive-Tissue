from pypylon import pylon
from pypylon import genicam
import matplotlib.pyplot as plt
import sys
import os
import methods as me
import serial
import time

def print_hi(name):
    # Open the serial connection
    print("Opening serial connection...")
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    print("Serial connection opened.")
    
    # Camera settings
    exitCode = 0
    file_path = r"/home/ilaig/project_final/Images/encoder_decoder_images"
    os.makedirs(file_path, exist_ok=True)
    print(f"Directory {file_path} created or already exists.")

    bmp_path = r"/home/ilaig/project_final/Images/mnist_photos_bmp" #r"/home/ilaig/project_final_code/system_exp/Images/image_org/bmp photos" #/home/ilaig/project_final_code/photos_bmp_waveshare/photos bmp"
    shake_hands = "A5 00 09 00 CC 33 C3 3C AC"
    set_storage = "A5 00 0A 07 01 CC 33 C3 3C A9"
    read_storage = "A5 00 09 06 CC 33 C3 3C A6"
    refresh = "A5 00 09 0A CC 33 C3 3C A6"
    load_image = "A5 00 09 0F CC 33 C3 3C A3"
    clear_screen = "A5 00 09 2E CC 33 C3 3C 82"
    
    try:
        # Collect photo files
        photo_files = [filename for filename in os.listdir(bmp_path)]
        print(f"Found {len(photo_files)} photo files.")
        photo_files.sort()

        file_of_command_path = r"/home/ilaig/project_final/command_waveshare.txt"
        
        # Start serial communication with waveshare screen
        first_commands = [shake_hands, set_storage, read_storage]

        # Write initial commands to the file
        with open(file_of_command_path, 'w') as f:
            for command in first_commands:
                f.write(command + '\n')

        # Send initial commands
        me.send_commands_from_file(file_of_command_path,ser)
        print("Initial commands sent to waveshare screen.")
        
        print("Creating camera object...")
        # Create an instant camera object with the camera device found first.
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        camera.Open()
        print("Camera opened successfully.")

        # Print the model name of the camera.
        print("Using device ", camera.GetDeviceInfo().GetModelName())
        # Set the exposure time and gain
        #camera.ExposureTime.SetValue(60000.0)  # Set exposure time in microseconds (e.g., 20000us = 20ms)
        camera.ExposureAuto.SetValue('Continuous')
        new_width = camera.Width.Value - camera.Width.Inc
        if new_width >= camera.Width.Min:
            camera.Width.Value = new_width
            print(f"Camera width set to {new_width}.")

        # The parameter MaxNumBuffer can be used to control the count of buffers
        # allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer = 5
        print("MaxNumBuffer set to 5.")
        count_camera=2
        # Start the grabbing of images.
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        #camera.StartGrabbing(pylon.GrabStrategy_OneByOne)

        print("Camera started grabbing images.")

        if not camera.IsGrabbing():
            print("Failed to start grabbing.")
            camera.Close()
            ser.close()
            sys.exit(1)

        # Prepare to grab images
        index_photo = 0
        time.sleep(0.5)
        #count=0
        for img in photo_files:
            #if count==2:
              #break
            #count+=1
            start_time = time.time()
            name_photo = os.path.basename(img)
            name_photo = os.path.splitext(name_photo)[0]  # take the first part in IM0.BMP --> take: IMO
            name_photo = me.convert_ascii_hexa(name_photo)
            length_command = me.count_len_command(f"A5 00 00 70 00 00 00 00 {name_photo} 2E 42 4D 50 00 CC 33 C3 3C 00")
            parity_byte = me.cal_parity_byte(f"A5 00 {length_command} 70 00 00 00 00 {name_photo} 2E 42 4D 50 00 CC 33 C3 3C 00")
            image = f"A5 00 {length_command} 70 00 00 00 00 {name_photo} 2E 42 4D 50 00 CC 33 C3 3C {parity_byte}"

            # Commands for each photo
            command_for_each_photo = [clear_screen, image, refresh]
            with open(file_of_command_path, 'w') as f:  # Use 'w' to overwrite the file
                for command in command_for_each_photo:
                    f.write(command + '\n')

            # Send all commands from the file for each photo
            me.send_commands_from_file(file_of_command_path,ser)
            print(f"Commands sent to display image: {img}")
            end_time=time.time()
            wait_time= end_time-start_time
            print (wait_time)
            # Wait for the image to be fully displayed on the screen
            time.sleep(4-wait_time)  # Adjust this delay as needed to ensure the image is fully displayed

            # Ensure the camera is still grabbing
            if camera.IsGrabbing():
                try:
                    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                    
                    # Check if image grab succeeded
                    if grabResult.GrabSucceeded():
                        print(f"Image {index_photo} grabbed successfully.")
                        img = grabResult.Array
                        file_output_img = os.path.join(file_path, f"IMG_{index_photo}.png")
                        plt.imsave(file_output_img, img, cmap='gray')
                        index_photo += 1
                        time.sleep(0.5)
                    else:
                        print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)
                        break
                    
                    # Release the grab result only if it is valid
                    if grabResult is not None:
                        grabResult.Release()
                except genicam.GenericException as e:
                    print(f"An error occurred while grabbing image {index_photo}: {e}")
            else:
                print("Camera is not grabbing.")

        camera.Close()
        print("Camera closed.")

        # Commands to clear and refresh the screen
        command_for_each_photo = [clear_screen, refresh]
        with open(file_of_command_path, 'w') as f:
            for command in command_for_each_photo:
                f.write(command + '\n')

        # Send all commands from the file to clear and refresh the screen
        me.send_commands_from_file(file_of_command_path,ser)
        print("Commands to clear and refresh the screen sent.")

    except genicam.GenericException as e:
        # Error handling.
        print("An exception occurred.")
        print(e)
        exitCode = 1

    # Close the serial connection
    ser.close()
    print("Serial connection closed.")

    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    sys.exit(exitCode)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
