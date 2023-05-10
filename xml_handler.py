from xml.etree import ElementTree as ET
from os import listdir
from re import findall


class XMLHandler(object):
    source_default_axis = 0
    target_default_axis = [7]

    def get_project_directory(self, path='C:\OMRON\Data\Solution', dateCreated='2023-04-27T15:18:53', ):
        """
        （弃用）
        通过给定Sysmac Studio创建的项目时间，在path目录下查找到该项目所在文件夹
        :param path: Sysmac Studio所有项目保存的目录，类型：str
        :param dateCreated: 项目的创建时间，格式必须为'2023-04-19T13:34:07'，类型：str
        :return: 返回项目所在的文件夹路径，如果没有找到则路径返回为空字符，类型：str
        """
        project_directory = listdir(path)
        # print(project_directory)
        find_ok = False
        project_path = ''
        for dic_name in project_directory:
            files = listdir(path + '\\' + dic_name)
            # print(files)
            if find_ok:
                break
            for file_name in files:
                match_list = findall(r'.+\.xml', file_name)
                # print(match_list)
                if len(match_list) != 0:
                    try:
                        tree = ET.parse(source=path + '\\' + dic_name + '\\' + file_name)
                    except Exception as e:
                        # print(e)
                        # print('xml加载打开失败！')
                        return project_path
                        pass
                    else:
                        root = tree.getroot()
                        elt = root.find('data/SolutionModel/DateCreated')
                        elt2 = root.find('data/SolutionModel/ProjectType')
                        if (elt is not None) and (elt2 is not None):
                            match_list1 = findall(dateCreated + r'\..*', elt.text)
                            if len(match_list1) != 0 and elt2.text == 'StandardProject':
                                project_path = path + '\\' + dic_name
                                print('项目目录：', project_path)
                                find_ok = True
                                break
        return project_path

    def get_project_directory1(self, path='C:\OMRON\Data\Solution', project_time='04/27/2023 15:18:53', is_dateCreated=True):
        """
        通过给定Sysmac Studio创建的项目时间，项目名称，在path目录下查找到该项目所在文件夹，返回项目所在文件夹和.oem文件的路径
        :param path: Sysmac Studio所有项目保存的目录，类型：str
        :param project_time: 项目的创建时间，格式必须为'04/19/2023 13:34:07'，类型：str
        :return: 返回项目所在的文件夹路径和.oem文件的路径，如果没有找到则路径返回为空字符，类型：str
        """
        project_directory = listdir(path)
        print(project_directory)
        find_ok = False
        project_path = ''
        oem_file_path = ''
        project_name = ''
        for dir_name in project_directory:
            files_path = listdir(path + '\\' + dir_name)
            if find_ok:
                break
            for fp in files_path:
                match_path = findall(r'.+\.oem', fp)
                # print(match_path)
                if len(match_path) != 0:
                    try:
                        tree = ET.parse(source=path + '\\' + dir_name + '\\' + fp)
                    except Exception as e:
                        # print(e)
                        print('.oem加载打开失败！')
                        return project_path, oem_file_path
                    else:
                        root = tree.getroot()
                        Entity_elt = root.find('./Entity')

                        s = ''
                        if is_dateCreated:
                            s = 'dateCreated'
                        else:
                            s = 'dateLastModified'

                        if Entity_elt.get(s) == project_time:
                            project_path = path + '\\' + dir_name
                            oem_file_path = path + '\\' + dir_name + '\\' + fp
                            project_name = Entity_elt.get('name')
                            print('项目目录：', project_path)
                            print('.oem文件路径：', oem_file_path)
                            find_ok = True
                            break
        if oem_file_path == '':
            print('没有匹配的.oem文件')
        return project_path, oem_file_path

    def get_axis_parameter_file_path(self, project_path):
        """
        （弃用）
        获取指定项目所有轴参数保存的文件路径，该方法只是用于项目中只有添加了一个控制器的情况
        :param project_path: 项目保存的路径，类型：str
        :return: 返回{ 轴号(int):轴参数保存的文件路径(str) }，类型：字典
        """
        axis_files_name = listdir(project_path)

        axis_file_path = {}  # 用于保存轴文件的路径比如 轴号(int):路径
        for file_name in axis_files_name:
            match_list = findall(r'.+\.xml', file_name)
            if len(match_list) != 0:
                try:
                    tree = ET.parse(source=project_path + '\\' + file_name)
                except Exception as e:
                    # print(e)
                    # print('加载XML失败！')
                    pass
                else:
                    root = tree.getroot()
                    AxisNumber_elt = root.find('NexAxisGeneralSetting/NexAxisAxisNumber/CurrentValue')
                    if AxisNumber_elt is not None:
                        # print(AxisNumber_elt.text)
                        axis_file_path[int(AxisNumber_elt.text)] = project_path + '\\' + file_name
        print(axis_file_path)
        return axis_file_path

    def get_axis_parameter_file_path1(self, oem_file_path, controller_name='new_Controller_2'):
        """
        通过项目的.oem文件和项目中添加的控制器名称，获取该控制器下所有轴参数保存的文件路径。适用于一个项目下添加了多个控制器的情况。
        :param oem_file_path: .oem文件的绝对路径，类型：str
        :param controller_name: 项目中控制器的名称，类型：str
        :return: axis_parameter_file_path为：{ 轴名:轴参数保存的文件路径(str) }，类型：字典，key为int类型
                 axis_parameter_file_path1为：{ 轴号:轴参数保存的文件路径(str) }，类型：字典，key为str类型
                 axis_name_list为：轴名字组成的列表，如：['MC_Axis000 (0)', 'MC_Axis001 (1)', 'MC_Axis002 (2)']
        """
        project_path = ''

        for i in oem_file_path.split('\\')[0:-1:]:
            project_path = project_path + i + '\\'

        axis_parameter_file_path = {}
        axis_parameter_file_path1 = {}
        axis_name_list = []
        try:
            tree = ET.parse(oem_file_path)
        except Exception as e:
            print(e)
            print('加载.oem文件失败！')
            return axis_parameter_file_path, axis_parameter_file_path1, axis_name_list
        else:
            root = tree.getroot()
            axis_setting_elts = root.findall("./Entity/ChildEntities/*[@name='{0:s}']"
                                             "/ChildEntities/*[@name='运动控制设置']/"
                                             "/ChildEntities/*[@type='AxesRootEntity']"
                                             "/ChildEntities/*[@type='AxisSettingEntity']".format(controller_name))
            # print(axis_setting_elts)
            if axis_setting_elts is not None:
                for axis_setting_elt in axis_setting_elts:
                    # print(axis_setting_elt.get('DN'), axis_setting_elt.get('id') + '.xml')
                    axis_parameter_file_path[axis_setting_elt.get('DN')] = project_path + '\\' + axis_setting_elt.get(
                        'id') + '.xml'

                axis_dict = {}
                axis_no_list = []
                for k in axis_parameter_file_path:
                    axis_no = int(findall(r'(?<=\()\d{1,3}(?=,|\))', k)[0])
                    axis_dict[axis_no] = k
                    axis_parameter_file_path1[axis_no] = axis_parameter_file_path[k]
                    axis_no_list.append(axis_no)
                axis_no_list.sort()

                for axis in axis_no_list:
                    axis_name_list.append(axis_dict[axis])
            else:
                print('未找到控制器%s' % controller_name)
        print('轴参数文件：', axis_parameter_file_path)
        print('轴参数文件1:', axis_parameter_file_path1)
        print('轴名列表', axis_name_list)

        return axis_parameter_file_path, axis_parameter_file_path1, axis_name_list

    def get_controller_name(self, oem_file_path):
        """
        获取项目名称和当前项目中添加的所有控制器的名字
        :param oem_file_path: .oem文件的绝对路径，类型str
        :return: 返回项目名称（类型：str）和当前项目中添加的所有控制器的名字组成的列表（类型：list）
        """
        project_name = ''
        controller_names = []
        try:
            tree = ET.parse(source=oem_file_path)
        except Exception as e:
            print(e)
            print('加载.oem文件失败！')
            return project_name, controller_names
        else:
            root = tree.getroot()
            project_name = root.find('./Entity').get('name')
            controller_elts = root.findall('./Entity/ChildEntities/Entity')[7::]  # 左右控制器元素

            for controller_elt in controller_elts:
                if controller_elt.findall(
                        "./ChildEntities/Entity/ChildEntities/*[@type='AxesRootEntity']") != []:  # 控制器元素是否包含运动控制设置（如果有HMI则不限在控制器名称中）
                    controller_names.append(controller_elt.get('name'))
            print('控制器名称:', controller_names)
            return project_name, controller_names

    def paste_pdo_parameter(self, axis_path: dict, is_axis_no=True, source=source_default_axis,
                            target=target_default_axis):
        """
        将指定轴的PDO粘贴到其他轴
        :param axis_path: 轴参数文件所在的路径，类型：dict { 轴号(int):轴参数保存的文件路径(str) }
        :param source: 复制轴的轴号，类型：int
        :param target: 粘贴轴的轴号，类型：list [轴号(int), 轴号(int), ...]
        """
        if axis_path != {}:
            source_tree = ET.parse(axis_path[source])
            source_AxisGeneralSetting_elt = source_tree.find('./NexAxisGeneralSetting')
            # target_trees = []
            for axis_NO in target:
                target_tree = ET.parse(axis_path[axis_NO])
                target_root = target_tree.getroot()
                target_AxisGeneralSetting_elt = target_root.find('./NexAxisGeneralSetting')
                out_device_value_elt = target_root.find('./NexAxisGeneralSetting/NexAxisOutputDevice1')
                for child in target_AxisGeneralSetting_elt:
                    match_tag = findall(r'PDO\d{1,2}.*', child.tag)
                    # print(match_tag)
                    if len(match_tag) != 0:
                        # children = child.find('./'+match_tag[0])
                        # print(children)
                        match_tag1 = findall(r'PDO\d{1,2}MappedDevice', match_tag[0])
                        # print(match_tag1)
                        if len(match_tag1) != 0:  # PDO1MappedDevice 元素不能用复制轴的参数覆盖
                            for child2, child3 in zip(child, out_device_value_elt):
                                child2.text = child3.text
                        else:
                            for child4, child5 in zip(child, source_AxisGeneralSetting_elt.find('./' + match_tag[0])):
                                child4.text = child5.text

                # target_tree.write(r'C:\Users\sqqian\Desktop\test\{0:d}'.format(axis_NO)+'.xml', encoding='utf-8')
                target_tree.write(axis_path[axis_NO], encoding='utf-8', xml_declaration=True)
        else:
            print('axis_path 为空字典，paste_pdo_parameter')

    def paste_unit_conversion_settings(self, axis_path: dict, is_axis_no=True, source=source_default_axis,
                                       target=target_default_axis):
        """
        将source指定轴的单位换算设置粘贴到target指定的轴中，同时修改轴设置中所有涉及单单位显示的内容
        :param axis_path: 轴参数文件所在的路径，类型：dict { 轴号(int):轴参数保存的文件路径(str) }
        :param source: 复制轴的轴号，类型：int
        :param target: 粘贴轴的轴号，类型：list [轴号(int), 轴号(int), ...]
        """
        if axis_path != {}:
            source_tree = ET.parse(axis_path[source])
            source_NexAxisScaling_elt = source_tree.find('./NexAxisScaling')
            source_root = source_tree.getroot()
            for axis_NO in target:
                target_tree = ET.parse(axis_path[axis_NO])
                target_root = target_tree.getroot()

                for target_child0, source_child0 in zip(target_root, source_root):
                    # for target_child0_1, source_child0_1 in zip(target_child0, source_child0):
                    if target_child0.tag == 'NexAxisScaling':  # 粘贴单位换算里的所有设置项
                        for target_child0_1, source_child0_1 in zip(target_child0, source_child0):
                            for target_child0_1_1, source_child0_1_1 in zip(target_child0_1, source_child0_1):
                                if target_child0_1_1.tag in ['CurrentValue', 'IsEnabled', 'IsVisible']:
                                    target_child0_1_1.text = source_child0_1_1.text
                    else:  # 变更轴设置里的所有项目的单位
                        for target_child0_1, source_child0_1 in zip(target_child0, source_child0):
                            match_tags = findall(r'.*Value2', target_child0_1.tag)
                            if len(match_tags) != 0:
                                for target_child0_1_1, source_child0_1_1 in zip(target_child0_1, source_child0_1):
                                    if target_child0_1_1.tag in ['CurrentValue', 'IsEnabled', 'IsVisible']:
                                        target_child0_1_1.text = source_child0_1_1.text
                # target_tree.write(r'C:\Users\sqqian\Desktop\{0:d}'.format(axis_NO)+'.xml', encoding='utf-8')
                target_tree.write(axis_path[axis_NO], encoding='utf-8', xml_declaration=True)
        else:
            print('axis_path 为空字典，paste_unit_conversion')

    def paste_operation_settings(self, axis_path: dict, is_axis_no=True, source=source_default_axis,
                                 target=target_default_axis):
        """
        将source指定轴的操作设置粘贴到target指定的轴中
        :param axis_path: 轴参数文件所在的路径，类型：dict { 轴号(int):轴参数保存的文件路径(str) }
        :param source: 复制轴的轴号，类型：int
        :param target: 粘贴轴的轴号，类型：list [轴号(int), 轴号(int), ...]
        """
        if axis_path != {}:
            source_tree = ET.parse(axis_path[source])
            source_NexAxisDynamics_elt = source_tree.find('./NexAxisDynamics')
            for axis_NO in target:
                target_tree = ET.parse(axis_path[axis_NO])
                target_root = target_tree.getroot()
                target_NexAxisDynamics_elt = target_root.find('./NexAxisDynamics')
                # for i in target_NexAxisScaling_elt:
                #     print(i)
                # print('*' * 50)
                for child, child2 in zip(target_NexAxisDynamics_elt, source_NexAxisDynamics_elt):
                    for child_1, child2_1 in zip(child, child2):
                        if child_1.tag in ['CurrentValue', 'IsEnabled', 'IsVisible']:
                            # print(child_1.text)
                            # print(child2_1.text)
                            child_1.text = child2_1.text
                # target_tree.write(r'C:\Users\sqqian\Desktop\{0:d}'.format(axis_NO) + '.xml', encoding='utf-8')
                target_tree.write(axis_path[axis_NO], encoding='utf-8', xml_declaration=True)
        else:
            print('axis_path 为空字典，paste_unit_conversion')

    def paste_other_operation_settings(self, axis_path: dict, is_axis_no=True, source=source_default_axis,
                                       target=target_default_axis):
        """
        将source指定轴的其他操作设置粘贴到target指定的轴中
        :param axis_path: 轴参数文件所在的路径，类型：dict { 轴号(int):轴参数保存的文件路径(str) }
        :param source: 复制轴的轴号，类型：int
        :param target: 粘贴轴的轴号，类型：list [轴号(int), 轴号(int), ...]
        """
        if axis_path != {}:
            source_tree = ET.parse(axis_path[source])
            source_NexAxisStopOptions_elt = source_tree.find('./NexAxisStopOptions')
            for axis_NO in target:
                target_tree = ET.parse(axis_path[axis_NO])
                target_root = target_tree.getroot()
                target_NexAxisStopOptions_elt = target_root.find('./NexAxisStopOptions')
                # for i in target_NexAxisScaling_elt:
                #     print(i)
                # print('*' * 50)
                for child, child2 in zip(target_NexAxisStopOptions_elt, source_NexAxisStopOptions_elt):
                    for child_1, child2_1 in zip(child, child2):
                        if child_1.tag in ['CurrentValue', 'IsEnabled', 'IsVisible']:
                            # print(child_1.text)
                            # print(child2_1.text)
                            child_1.text = child2_1.text
                # target_tree.write(r'C:\Users\sqqian\Desktop\{0:d}'.format(axis_NO) + '.xml', encoding='utf-8')
                target_tree.write(axis_path[axis_NO], encoding='utf-8', xml_declaration=True)
        else:
            print('axis_path 为空字典，paste_unit_conversion')

    def paste_limits_settings(self, axis_path: dict, is_axis_no=True, source=source_default_axis,
                              target=target_default_axis):
        """
        将source指定轴的限位设置粘贴到target指定的轴中
        :param axis_path: 轴参数文件所在的路径，类型：dict { 轴号(int):轴参数保存的文件路径(str) }
        :param source: 复制轴的轴号，类型：int
        :param target: 粘贴轴的轴号，类型：list [轴号(int), 轴号(int), ...]
        """
        if axis_path != {}:
            source_tree = ET.parse(axis_path[source])
            source_NexAxisLimits_elt = source_tree.find('./NexAxisLimits')
            for axis_NO in target:
                target_tree = ET.parse(axis_path[axis_NO])
                target_root = target_tree.getroot()
                target_NexAxisLimits_elt = target_root.find('./NexAxisLimits')
                # for i in target_NexAxisScaling_elt:
                #     print(i)
                # print('*' * 50)
                for child, child2 in zip(target_NexAxisLimits_elt, source_NexAxisLimits_elt):
                    for child_1, child2_1 in zip(child, child2):
                        if child_1.tag in ['CurrentValue', 'IsEnabled', 'IsVisible']:
                            # print(child_1.text)
                            # print(child2_1.text)
                            child_1.text = child2_1.text
                # target_tree.write(r'C:\Users\sqqian\Desktop\{0:d}'.format(axis_NO) + '.xml', encoding='utf-8')
                target_tree.write(axis_path[axis_NO], encoding='utf-8', xml_declaration=True)
        else:
            print('axis_path 为空字典，paste_unit_conversion')

    def paste_homing_settings(self, axis_path: dict, is_axis_no=True, source=source_default_axis,
                              target=target_default_axis):
        """
        将source指定轴的原点返回设置粘贴到target指定的轴中
        :param axis_path: 轴参数文件所在的路径，类型：dict { 轴号(int):轴参数保存的文件路径(str) }
        :param source: 复制轴的轴号，类型：int
        :param target: 粘贴轴的轴号，类型：list [轴号(int), 轴号(int), ...]
        """
        if axis_path != {}:
            source_tree = ET.parse(axis_path[source])
            source_NexAxisHoming_elt = source_tree.find('./NexAxisHoming')
            for axis_NO in target:
                target_tree = ET.parse(axis_path[axis_NO])
                target_root = target_tree.getroot()
                target_NexAxisHoming_elt = target_root.find('./NexAxisHoming')
                # for i in target_NexAxisScaling_elt:
                #     print(i)
                # print('*' * 50)
                for child, child2 in zip(target_NexAxisHoming_elt, source_NexAxisHoming_elt):
                    for child_1, child2_1 in zip(child, child2):
                        if child_1.tag in ['CurrentValue', 'IsEnabled', 'IsVisible']:
                            # print(child_1.text)
                            # print(child2_1.text)
                            child_1.text = child2_1.text
                # target_tree.write(r'C:\Users\sqqian\Desktop\{0:d}'.format(axis_NO) + '.xml', encoding='utf-8')
                target_tree.write(axis_path[axis_NO], encoding='utf-8', xml_declaration=True)
        else:
            print('axis_path 为空字典，paste_unit_conversion')

    def paste_position_count_settings(self, axis_path: dict, is_axis_no=True, source=source_default_axis,
                                      target=target_default_axis):
        """
        将source指定轴的位置计数设置粘贴到target指定的轴中
        :param axis_path: 轴参数文件所在的路径，类型：dict { 轴号(int):轴参数保存的文件路径(str) }
        :param source: 复制轴的轴号，类型：int
        :param target: 粘贴轴的轴号，类型：list [轴号(int), 轴号(int), ...]
        """
        if axis_path != {}:
            source_tree = ET.parse(axis_path[source])
            source_NexAxisCount_elt = source_tree.find('./NexAxisCount')
            for axis_NO in target:
                target_tree = ET.parse(axis_path[axis_NO])
                target_root = target_tree.getroot()
                target_NexAxisCount_elt = target_root.find('./NexAxisCount')
                # for i in target_NexAxisScaling_elt:
                #     print(i)
                # print('*' * 50)
                for child, child2 in zip(target_NexAxisCount_elt, source_NexAxisCount_elt):
                    for child_1, child2_1 in zip(child, child2):
                        if child_1.tag in ['CurrentValue', 'IsEnabled', 'IsVisible']:
                            # print(child_1.text)
                            # print(child2_1.text)
                            child_1.text = child2_1.text
                # target_tree.write(r'C:\Users\sqqian\Desktop\{0:d}'.format(axis_NO) + '.xml', encoding='utf-8')
                target_tree.write(axis_path[axis_NO], encoding='utf-8', xml_declaration=True)
        else:
            print('axis_path 为空字典，paste_unit_conversion')

    def paste_servo_driver_settings(self, axis_path: dict, is_axis_no=True, source=source_default_axis,
                                    target=target_default_axis):
        """
        将source指定轴的伺服驱动器设置粘贴到target指定的轴中
        :param axis_path: 轴参数文件所在的路径，类型：dict { 轴号(int):轴参数保存的文件路径(str) }
        :param source: 复制轴的轴号，类型：int
        :param target: 粘贴轴的轴号，类型：list [轴号(int), 轴号(int), ...]
        """
        if axis_path != {}:
            source_tree = ET.parse(axis_path[source])
            source_NexAxisServoDriverSetting_elt = source_tree.find('./NexAxisServoDriverSetting')
            for axis_NO in target:
                target_tree = ET.parse(axis_path[axis_NO])
                target_root = target_tree.getroot()
                target_NexAxisServoDriverSetting_elt = target_root.find('./NexAxisServoDriverSetting')
                # for i in target_NexAxisScaling_elt:
                #     print(i)
                # print('*' * 50)
                for child, child2 in zip(target_NexAxisServoDriverSetting_elt, source_NexAxisServoDriverSetting_elt):
                    for child_1, child2_1 in zip(child, child2):
                        if child_1.tag in ['CurrentValue', 'IsEnabled', 'IsVisible']:
                            # print(child_1.text)
                            # print(child2_1.text)
                            child_1.text = child2_1.text
                # target_tree.write(r'C:\Users\sqqian\Desktop\{0:d}'.format(axis_NO) + '.xml', encoding='utf-8')
                target_tree.write(axis_path[axis_NO], encoding='utf-8', xml_declaration=True)
        else:
            print('axis_path 为空字典，paste_unit_conversion')


if __name__ == '__main__':
    xml_handler = XMLHandler()
    # project_path = xml_handler.get_project_directory()
    project_path, oem_file_path = xml_handler.get_project_directory1()
    axis_parameter_file_path, axis_parameter_file_path1, axis_name_list = xml_handler.get_axis_parameter_file_path1(
        oem_file_path)
    # axis_files = xml_handler.get_axis_parameter_file_path(project_path)
    # xml_handler.copy_parameter(axis_path={0: 'C:\\OMRON\\Data\\Solution\\1914ddb1-6484-4f81-b232-2d4273ab4c11'
    #                                          '\\54b60214-5d73-4432-bdcb-f7e8256a678f.xml',
    #                                       1: 'C:\\OMRON\\Data\\Solution\\1914ddb1-6484-4f81-b232-2d4273ab4c11'
    #                                          '\\7dffd4a2-7073-40fb-9025-e5f6182c2627.xml',
    #                                       2: 'C:\\OMRON\\Data\\Solution\\1914ddb1-6484-4f81-b232-2d4273ab4c11'
    #                                          '\\7e390743-330f-42a2-8f84-cf4dd821bc63.xml'},
    #                            source=0,
    #                            target=[1, 2])
    project_name, controller_names = xml_handler.get_controller_name(oem_file_path)
    xml_handler.paste_pdo_parameter(axis_path=axis_parameter_file_path1)
    xml_handler.paste_unit_conversion_settings(axis_path=axis_parameter_file_path1)
    xml_handler.paste_operation_settings(axis_path=axis_parameter_file_path1)
    xml_handler.paste_other_operation_settings(axis_path=axis_parameter_file_path1)
    xml_handler.paste_limits_settings(axis_path=axis_parameter_file_path1)
    xml_handler.paste_homing_settings(axis_path=axis_parameter_file_path1)
    xml_handler.paste_position_count_settings(axis_path=axis_parameter_file_path1)
    xml_handler.paste_servo_driver_settings(axis_path=axis_parameter_file_path1)
