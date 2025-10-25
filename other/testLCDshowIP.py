import serial,time,psutil,socket
from PIL import Image, ImageDraw, ImageFont  # Import PIL library for image processing
from datetime import datetime, timedelta  # For getting current time
import serial.tools.list_ports as list_ports

# RGB565 color encoding
RED = 0xf800
GREEN = 0x07e0
BLUE = 0x001f
WHITE = 0xffff
BLACK = 0x0000
YELLOW = 0xFFE0
GRAY0 = 0xEF7D
GRAY1 = 0x8410
GRAY2 = 0x4208

size_USE_X1=160
size_USE_Y1=80

State_change = 1  # State changed
def SER_Read():
    global Device_State
    # print('Receiving data');
    try:  # Try to get data
        Data_U1 = ser.read(ser.in_waiting)
        return Data_U1
    except:  # Exception occurred
        # print('Receive exception');
        Device_State = 0
        ser.close()  # Close serial port to prevent next open failure
        return 0
com_name=""

# Try to find COM port with retry logic
max_retries = 3
retry_count = 0

while retry_count < max_retries and com_name == "":
    port_list = list(list_ports.comports())  # Query all serial ports
    
    if len(port_list) == 0:
        retry_count += 1
        if retry_count < max_retries:
            print(f'No serial port detected (attempt {retry_count}/{max_retries}), waiting 2 seconds...')
            time.sleep(2)
        else:
            print('\n' + '='*60)
            print('ERROR: No COM ports found on this system')
            print('='*60)
            print('Please check:')
            print('  1. Device is properly connected to the computer')
            print('  2. Device drivers are installed')
            print('  3. Device is powered on')
            print('='*60)
            input('Press Enter to exit...')
            exit(1)
    else:  # Monitor serial ports to ensure MSN device
        for i in range(0, len(port_list)):
            try:  # Try to open serial port
                ser = serial.Serial(port_list[i].name, 19200, timeout=2)  # Initialize serial connection
            except:  # Exception occurred
                print(port_list[i].name + ' cannot be opened, check if used by other programs')
                # ser.close()  # Close serial port to prevent next open failure
                time.sleep(0.1)
                continue  # Execute next loop
            time.sleep(0.25)  # Theoretically MSN device sends "MSN01" every 100ms, should receive at least once in 250ms
            recv = SER_Read()
            print(len(recv))
            if len(recv)>10:
                print("found device, PORT:",port_list[i].name)
                com_name=port_list[i].name
                ser.close()
                break
            else:
                ser.close()
        
        # If device not found in this attempt, retry
        if com_name == "":
            retry_count += 1
            if retry_count < max_retries:
                print(f'MSN device not found (attempt {retry_count}/{max_retries}), waiting 2 seconds...')
                time.sleep(2)

# Final check if device was found
if com_name == "":
    print('\n' + '='*60)
    print('ERROR: MSN device not detected')
    print('='*60)
    print('COM ports found but no MSN device responded.')
    print('Please check:')
    print('  1. Device is the correct MSN model')
    print('  2. Device firmware is functioning properly')
    print('  3. Try unplugging and reconnecting the device')
    print('='*60)
    input('Press Enter to exit...')
    exit(1)

print(f"\nSuccessfully connected to MSN device on port: {com_name}")

State_change = 1  # State changed
ser=serial.Serial(com_name,19200,timeout=0.5)
print(ser.is_open)

def LCD_Set_Color(LCD_D0, LCD_D1):  # Set color (FC,BC)
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(2).to_bytes(1, byteorder="little")  # Set color
    hex_use = hex_use + int(LCD_D0 // 256).to_bytes(1, byteorder="little")  # Data0
    hex_use = hex_use + int(LCD_D0 % 256).to_bytes(1, byteorder="little")  # Data1
    hex_use = hex_use + int(LCD_D1 // 256).to_bytes(1, byteorder="little")  # Data2
    hex_use = hex_use + int(LCD_D1 % 256).to_bytes(1, byteorder="little")  # Data3
    SER_Write(hex_use)  # Send command

def LCD_Set_Size(LCD_D0, LCD_D1):  # Set size
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(1).to_bytes(1, byteorder="little")  # Set size
    hex_use = hex_use + int(LCD_D0 // 256).to_bytes(1, byteorder="little")  # Data0
    hex_use = hex_use + int(LCD_D0 % 256).to_bytes(1, byteorder="little")  # Data1
    hex_use = hex_use + int(LCD_D1 // 256).to_bytes(1, byteorder="little")  # Data2
    hex_use = hex_use + int(LCD_D1 % 256).to_bytes(1, byteorder="little")  # Data3
    SER_Write(hex_use)  # Send command
 
def SER_Write(Data_U0):
    global Device_State
    # print('Sending data');
    try:  # Try to send command, two cases of failed command: 1.Device removed, send error; 2.Device in MSN connection state, slow response to PC commands
        # Timeout detection
        # u_time=time.time()
        if (False == ser.is_open):
            Device_State = 0  # Return to unconnected state
        ser.write(Data_U0)
        # print(Data_U0)
        # u_time=time.time()-u_time
        # if u_time>2:
        # print('Send timeout');
        # Device_State=0  # Return to unconnected state
        # ser.close()  # Close serial port to prevent next open failure
        # else:
        # print('Send complete');
    except:  # Exception occurred
        # print('Send exception');
        Device_State = 0
        ser.close()  # Close serial port to prevent next open failure

def LCD_Set_XY(LCD_D0, LCD_D1):  # Set start position
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")  # Set start position
    hex_use = hex_use + int(LCD_D0 // 256).to_bytes(1, byteorder="little")  # Data0
    hex_use = hex_use + int(LCD_D0 % 256).to_bytes(1, byteorder="little")  # Data1
    hex_use = hex_use + int(LCD_D1 // 256).to_bytes(1, byteorder="little")  # Data2
    hex_use = hex_use + int(LCD_D1 % 256).to_bytes(1, byteorder="little")  # Data3
    SER_Write(hex_use)  # Send command

def LCD_Photo(LCD_X, LCD_Y, LCD_X_Size, LCD_Y_Size, Page_Add):  #
    global Device_State
    LCD_Set_XY(LCD_X, LCD_Y)
    LCD_Set_Size(LCD_X_Size, LCD_Y_Size)
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # Set command
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")  # Display color image
    hex_use = hex_use + int(Page_Add // 256).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(Page_Add % 256).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        time.sleep(0.001)
        recv = SER_Read()  # .decode("UTF-8")  # Get serial port data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            if ((recv[0] != hex_use[0]) or (recv[1] != hex_use[1])):
                Device_State = 0  # Receive error
            break
            
           
def LCD_ASCII_32X64_MIX(LCD_X, LCD_Y, Txt, LCD_FC, BG_Page, Num_Page):  #
    global Device_State
    LCD_Set_XY(LCD_X, LCD_Y)
    LCD_Set_Color(LCD_FC, BG_Page)
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # Set command
    hex_use = hex_use + int(5).to_bytes(1, byteorder="little")  # Display ASCII
    hex_use = hex_use + int(ord(Txt)).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(Num_Page // 256).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(Num_Page % 256).to_bytes(1, byteorder="little")
    SER_Write(hex_use)  # Send command
    print(hex_use)
    # Wait for response
    while (1):
        # time.sleep(0.5)
        recv = SER_Read()  # .decode("UTF-8")  # Get serial port data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            if ((recv[0] != hex_use[0]) or (recv[1] != hex_use[1])):
                Device_State = 0  # Receive error
            break

def show_PC_time():
    global State_change
    FC = YELLOW
    photo_add = 3826
    num_add = 3651
    if (State_change == 1):
        State_change = 0
        LCD_Photo(0, 0, 160, 80, photo_add)  # Place background
        # while(1):
        #    time.sleep(1)
        LCD_ASCII_32X64_MIX(56 + 8, 8, ':', FC, photo_add, num_add)
        
        # LCD_ASCII_32X64_MIX(136+8,32,':',FC,photo_add,num_add)
    if (State_change == 0):
        time_h = int(datetime.now().hour)
        time_m = int(datetime.now().minute)
        time_S = int(datetime.now().second)

        
        LCD_ASCII_32X64_MIX(0 + 8, 8, chr((time_h // 10) + 48), FC, photo_add, num_add)
        LCD_ASCII_32X64_MIX(32 + 8, 8, chr((time_h % 10) + 48), FC, photo_add, num_add)
        LCD_ASCII_32X64_MIX(80 + 8, 8, chr((time_m // 10) + 48), FC, photo_add, num_add)
        LCD_ASCII_32X64_MIX(112 + 8, 8, chr((time_m % 10) + 48), FC, photo_add, num_add)
        # LCD_ASCII_32X64_MIX(160+8,8,chr((time_S//10)+48),FC,photo_add,num_add)
        # LCD_ASCII_32X64_MIX(192+8,8,chr((time_S%10)+48),FC,photo_add,num_add)
        time.sleep(0.2)


def LCD_ADD(LCD_X, LCD_Y, LCD_X_Size, LCD_Y_Size):  #
    global Device_State
    LCD_Set_XY(LCD_X, LCD_Y)
    LCD_Set_Size(LCD_X_Size, LCD_Y_Size)
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # Set command
    hex_use = hex_use + int(7).to_bytes(1, byteorder="little")  # Load address
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        time.sleep(0.001)
        recv = SER_Read()  # .decode("UTF-8")  # Get serial port data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            if ((recv[0] != hex_use[0]) or (recv[1] != hex_use[1])):
                Device_State = 0  # Receive error
            break

def Screen_Date_Process(Photo_data):  # Process and convert data
    Photo_data_use = Photo_data
    hex_use = bytearray()  # Empty array
    for j in range(0, size_USE_X1 * size_USE_Y1 // 128):  # Write one Page at a time
        data_w = Photo_data_use[:128]
        Photo_data_use = Photo_data_use[128:]
        cmp_use = []  # Empty array
        for i in range(0, 64):  # 256 bytes divided into 64 commands
            cmp_use.append(data_w[i * 2 + 0] * 65536 + data_w[i * 2 + 1])
        result = max(set(cmp_use), key=cmp_use.count)  # Count most frequent data
        hex_use.append(2)
        hex_use.append(4)
        color_ram = result
        hex_use.append(color_ram >> 24)
        color_ram = color_ram % 16777216
        hex_use.append(color_ram >> 16)
        color_ram = color_ram % 65536
        hex_use.append(color_ram >> 8)
        hex_use.append(color_ram % 256)
        # Convert data format first
        for i in range(0, 64):  # 256 bytes divided into 64 commands
            if ((data_w[i * 2 + 0] * 65536 + data_w[i * 2 + 1]) != result):
                hex_use.append(4)
                hex_use.append(i)
                hex_use.append(data_w[i * 2 + 0] >> 8)
                hex_use.append(data_w[i * 2 + 0] % 256)
                hex_use.append(data_w[i * 2 + 1] >> 8)
                hex_use.append(data_w[i * 2 + 1] % 256)
        hex_use.append(2)
        hex_use.append(3)
        hex_use.append(8)
        hex_use.append(1)
        hex_use.append(0)
        hex_use.append(0)
    if (size_USE_X1 * size_USE_Y1 * 2 % 256 != 0):  # Still have unwritten data
        data_w = Photo_data_use  # Read remaining data
        for i in range(size_USE_X1 * size_USE_Y1 * 2 % 256, 256):
            data_w.append(0xffff)  # Fill insufficient positions with 0xFFFF
        for i in range(0, 64):  # 256 bytes divided into 64 commands
            hex_use.append(4)
            hex_use.append(i)
            hex_use.append(data_w[i * 2 + 0] >> 8)
            hex_use.append(data_w[i * 2 + 0] % 256)
            hex_use.append(data_w[i * 2 + 1] >> 8)
            hex_use.append(data_w[i * 2 + 1] % 256)
        hex_use.append(2)
        hex_use.append(3)
        hex_use.append(8)
        hex_use.append(0)
        hex_use.append(size_USE_X1 * size_USE_Y1 * 2 % 256)
        hex_use.append(0)
    return hex_use

netspeed_last_refresh_time = None
netspeed_last_refresh_snetio = None
netspeed_plot_data = None
def sizeof_fmt(num, suffix="B", base=1024.0):
    # Use KiB for small value
    if abs(num) < base:
        return f"{num / base:3.1f}Ki{suffix}"
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < base:
            return f"{num:3.1f}{unit}{suffix}"
        num /= base
    return f"{num:.1f}Yi{suffix}"

def get_ip_address():
    try:
        # Get the actual IP address by connecting to an external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "No Network"
        
def show_netspeed(text_color=(255, 128, 0)):
    # geezmo: Pre-render image, display network speed
    global netspeed_last_refresh_time, netspeed_last_refresh_snetio, netspeed_plot_data, State_change
    
    if netspeed_last_refresh_time is None or State_change == 1:
        # Initialize
        State_change = 0
        netspeed_last_refresh_time = datetime.now()
        netspeed_last_refresh_snetio = psutil.net_io_counters()
        netspeed_plot_data = [{'sent': 0, 'recv': 0}] * 120  # Store 120 slots of plot data
        # At initialization, network speed displays 0 first
        current_snetio = netspeed_last_refresh_snetio
    else:
        current_snetio = psutil.net_io_counters()
    
    # Get network speed bytes/second
    
    current_time = datetime.now()
    seconds_elapsed = (current_time - netspeed_last_refresh_time) / timedelta(seconds=1)
    
    sent_per_second = (current_snetio.bytes_sent - netspeed_last_refresh_snetio.bytes_sent) / seconds_elapsed
    recv_per_second = (current_snetio.bytes_recv - netspeed_last_refresh_snetio.bytes_recv) / seconds_elapsed
    # print(current_snetio.bytes_sent, netspeed_last_refresh_snetio.bytes_sent, seconds_elapsed)
    
    netspeed_plot_data = netspeed_plot_data[1:] + [{
        'sent': sent_per_second,
        'recv': recv_per_second,
    }]
    
    netspeed_last_refresh_time = current_time
    netspeed_last_refresh_snetio = current_snetio
    
    # Draw image
    
    im1 = Image.new('RGB', (size_USE_X1, size_USE_Y1), (0, 0, 0))
    # im1 = Image.open('example.png')
    
    draw = ImageDraw.Draw(im1)
    font_size = 16
    try:
        font = ImageFont.truetype("resource/Orbitron-Regular.ttf", font_size)
    except OSError:
        # Pillow may not ignore case sensitivity, to avoid read failure
        font = ImageFont.truetype("resource/Orbitron-Regular.ttf", font_size)
    
    # Draw text
    
    text = f"Up {sizeof_fmt(sent_per_second):>8}"
    draw.text((0, 0), text, fill=(255, 0, 0), font=font)
    
    # text = time.strftime('%Y%m%d  %H:%M:%S',time.localtime())
    # draw.text((0, 20), text, fill=(0,255, 0), font=font)
    
    text = f"Down {sizeof_fmt(recv_per_second):>8}"
    draw.text((0, 20), text, fill=(0,0,255), font=font)
    
    text = f"{get_ip_address()}"
    font = ImageFont.truetype("resource/Orbitron-Regular.ttf", 18)
    draw.text((0, 45), text, fill=text_color, font=font)

    # Drawing
    if 0:
        for start_y, key, color in zip([19, 59], ['sent', 'recv'], [(235, 139, 139), (146, 211, 217)]):
            sent_values = [data[key] for data in netspeed_plot_data]

            max_value = max(1024 * 100, max(sent_values))  # Minimum range 100KB/s
            bar_width = 2  # Width of each point
            image_height = 20  # Height
            
            for i, sent in enumerate(sent_values[-80:]):
                # Scale the sent value to the image height
                bar_height = int((sent / max_value) * image_height) if max_value else 0
                x0 = i * bar_width
                y0 = image_height - bar_height
                x1 = (i + 1) * bar_width
                y1 = image_height

                # Draw the bar
                draw.rectangle([x0, start_y + y0, x1 - 1, max(start_y + y0, start_y + y1 - 1)], fill=color)  # Green bars

    
    im2 = im1.load()
    
    hex_16RGB = []  # bytearray()
    
    for y in range(0, size_USE_Y1):
        for x in range(0, size_USE_X1):
            hex_16RGB.append(
                ((im2[x, y][0] >> 3) << 11) | ((im2[x, y][1] >> 2) << 5) | (im2[x, y][2] >> 3))  # Directly add 16bit array
    hexstream = Screen_Date_Process(hex_16RGB)
    LCD_ADD((160 - size_USE_X1) // 2, (80 - size_USE_Y1) // 2, size_USE_X1, size_USE_Y1)
    SER_Write(hexstream)
    
    # Refresh approximately every 1 second
    time.sleep(1 - (datetime.now() - netspeed_last_refresh_time) / timedelta(seconds=1))



hex_code = int(0).to_bytes(1, byteorder="little")  # Can add to array one by one
hex_code = hex_code + b'MSNCN'
SER_Write(hex_code)  # Return message
# Wait for return message, confirm connection
time.sleep(0.25)  # Theoretically MSN device sends "MSN01" every 100ms, should receive at least once in 250ms
        
while 1:
    # if State_change==1:
        # State_change=0
    # else:
        # State_change=1
    # show_PC_time()
    # time.sleep(0.5)
    show_netspeed()