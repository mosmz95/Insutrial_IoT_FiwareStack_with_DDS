from setuptools import find_packages, setup
from glob import glob
import os
package_name = 'defective_pcb_detector'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'configs'), glob('configs/*')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
    ],
    install_requires=['setuptools','requests',],
    zip_safe=True,
    maintainer='mostafa',
    maintainer_email='mostafa@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'defective_pcb_publisher    = defective_pcb_detector.defective_pcb_publisher:main',
            'defective_pcb_listener     = defective_pcb_detector.defective_pcb_listener:main',
            'defective_pcb_to_server    = defective_pcb_detector.defective_pcb_to_server:main',
            'random_pcb_publisher       = defective_pcb_detector.random_costum_publisher:main'
        ],
    },
)
