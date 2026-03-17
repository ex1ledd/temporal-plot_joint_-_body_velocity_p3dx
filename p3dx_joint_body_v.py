import time
import math
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# 1. Setup Connection
client = RemoteAPIClient()
sim = client.require('sim')

# 2. Start Simulation
sim.startSimulation()
print("Simulation Started")

# 3. Initialize Handles and Constants
sim.addLog(1, "Laurensius Duta Wicaksono | 5022231070 | Pengambilan Data...")
p3dx_RW = sim.getObject("/PioneerP3DX/rightMotor")
p3dx_LW = sim.getObject("/PioneerP3DX/leftMotor")

rw = 0.195/2  # wheel radius
rb = 0.381/2  # body radius

# Data storage for plotting
time_hist = []
wr_vel_hist = []
wl_vel_hist = []
vx_hist = []
wx_hist = []

try:
    # 4. Main Loop (Set to 30 seconds as per your current code)
    start_time = time.time()
    duration = 15 
    
    while (time.time() - start_time) < duration:
        elapsed = time.time() - start_time
        
        # Get target velocities (following teacher's method) [cite: 114]
        wr_vel = sim.getJointTargetVelocity(p3dx_RW)
        wl_vel = sim.getJointTargetVelocity(p3dx_LW)
        
        # Calculate body velocity using teacher's formula snippet [cite: 120, 122]
        vx = (wr_vel + wl_vel) * rw / rb
        wx = (wr_vel - wl_vel) * rw / rb

        # Append data to lists
        time_hist.append(elapsed)
        wr_vel_hist.append(wr_vel)
        wl_vel_hist.append(wl_vel)
        vx_hist.append(vx)
        wx_hist.append(wx)

        print(f"Running... {elapsed:.1f}s | Vx: {vx:.2f}", end="\r")
        time.sleep(0.1) 

finally:
    # 5. Stop Simulation safely
    sim.stopSimulation()
    print("\nSimulation Stopped. Generating Plots...")

    # 6. Plotting - Single window, two separate subplots 
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.tight_layout(pad=5.0)

    # Top Plot: Joint Velocities
    ax1.plot(time_hist, wr_vel_hist, label=r'$\dot{\phi}_R$ (Right)')
    ax1.plot(time_hist, wl_vel_hist, label=r'$\dot{\phi}_L$ (Left)')
    ax1.set_title('P3DX Joint Velocity')
    ax1.set_xlabel('Time (sec)')
    ax1.set_ylabel('Velocity (rad/s)')
    ax1.legend()
    ax1.grid(True)

    # Bottom Plot: Body Velocities
    ax2.plot(time_hist, vx_hist, label='$V_x$ (Linear)', color='green')
    ax2.plot(time_hist, wx_hist, label='$ω$ (Angular)', color='red')
    ax2.set_title('P3DX Body Velocity')
    ax2.set_xlabel('Time (sec)')
    ax2.set_ylabel('Velocity (m/s or rad/s)')
    ax2.legend()
    ax2.grid(True)

    plt.show()