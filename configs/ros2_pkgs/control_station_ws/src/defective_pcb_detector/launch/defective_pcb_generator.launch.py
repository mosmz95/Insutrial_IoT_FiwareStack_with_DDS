from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction,LogInfo
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    pcb_server_ip = LaunchConfiguration('pcb_server_ip')
    pcb_server_port = LaunchConfiguration('pcb_server_port')
    # pcb_server_url = PythonExpression([
    #     "'http://'", pcb_server_ip, "':'", pcb_server_port
    # ])
    return LaunchDescription([
        DeclareLaunchArgument(
            'pcb_server_ip',
            default_value='0.0.0.0'
        ),
        DeclareLaunchArgument(
            'pcb_server_port',
            default_value='5000'
        ), 
        # LogInfo(msg=PythonExpression([
        #     "'Launching FastAPI at http://' + str(", pcb_server_ip, ") + ':' + str(", pcb_server_port, ")"
        # ])),
        # ExecuteProcess(
        #     cmd=[[
        #         'python3 ', '-m ', 'uvicorn ',
        #         'pcb_img_server.run_server:app',
        #         ' --host ',pcb_server_ip,
        #         ' --port ',pcb_server_port
        #     ]],
        #     shell=True
        # ),

        Node(
            package='defective_pcb_detector',
            executable='defective_pcb_publisher',
            output='screen'
        ),

        Node(
            package='defective_pcb_detector',
            executable='defective_pcb_to_server',
            arguments= [['http://',pcb_server_ip,':',pcb_server_port]],
            output='screen'
        ),
        
    ])