from setuptools import setup

package_name = '4ze_vehicle_can'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'can_udp_bridge = 4ze_vehicle_can.can_udp_bridge:main',
        ],
    },
)
