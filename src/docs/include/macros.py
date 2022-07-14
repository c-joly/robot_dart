
def define_env(env):
    variables = {'INIT_SIMU': '\t```cpp\n\t// choose time step of 0.001 seconds\n\trobot_dart::RobotDARTSimu simu(0.001);\n\t```', 'MODIFY_SIMU_DT': '\t```cpp\n\t// set timestep to 0.005 and update control frequency(bool)\n\tsimu.set_timestep(0.005, true);\n\t```', 'SIMU_GRAVITY': '\t```cpp\n\t// Set gravitational force of mars\n\tEigen::Vector3d mars_gravity = {0., 0., -3.721};\n\tsimu.set_gravity(mars_gravity);\n\t```', 'SHADOWS_GRAPHICS': '\t```cpp\n\t// Disable shadows\n\tgraphics->enable_shadows(false, false);\n\tsimu.run(1.);\n\t// Enable non-transparent shadows\n\tgraphics->enable_shadows(true, false);\n\tsimu.run(1.);\n\t// Enable transparent shadows\n\tgraphics->enable_shadows(true, true);\n\tsimu.run(1.);\n\t```', 'CLR_LIGHT': '\t```cpp\n\t// Clear Lights\n\tgraphics->clear_lights();\n\t```', 'LIGHT_MATERIAL': '\t```cpp\n\t// Create Light material\n\tMagnum::Float shininess = 1000.f;\n\tMagnum::Color4 white = {1.f, 1.f, 1.f, 1.f};\n\t\n\t// ambient, diffuse, specular\n\tauto custom_material = robot_dart::gui::magnum::gs::Material(white, white, white, shininess);\n\t```', 'POINT_LIGHT': '\t```cpp\n\t// Create point light\n\tMagnum::Vector3 position = {0.f, 0.f, 2.f};\n\tMagnum::Float intensity = 1.f;\n\tMagnum::Vector3 attenuation_terms = {1.f, 0.f, 0.f};\n\tauto point_light = robot_dart::gui::magnum::gs::create_point_light(position, custom_material, intensity, attenuation_terms);\n\tgraphics->add_light(point_light);\n\t```', 'DIRECTIONAL_LIGHT': '\t```cpp\n\t// Create directional light\n\tMagnum::Vector3 direction = {-1.f, -1.f, -1.f};\n\tauto directional_light = robot_dart::gui::magnum::gs::create_directional_light(direction, custom_material);\n\tgraphics->add_light(directional_light);\n\t```', 'SPOT_LIGHT': '\t```cpp\n\t// Create spot light\n\tMagnum::Vector3 position = {0.f, 0.f, 1.f};\n\tMagnum::Vector3 direction = {-1.f, -1.f, -1.f};\n\tMagnum::Float intensity = 1.f;\n\tMagnum::Vector3 attenuation_terms = {1.f, 0.f, 0.f};\n\tMagnum::Float spot_exponent = M_PI;\n\tMagnum::Float spot_cut_off = M_PI / 8;\n\tauto spot_light = robot_dart::gui::magnum::gs::create_spot_light(position, custom_material, direction, spot_exponent, spot_cut_off, intensity, attenuation_terms);\n\t```', 'RECORD_VIDEO_ROBOT_GRAPHICS_PARAMS': '\t```cpp\n\trobot_dart::gui::magnum::GraphicsConfiguration configuration;\n\tconfiguration.width = 1280;\n\tconfiguration.height = 960;\n\tconfiguration.bg_color = Eigen::Vector4d{1.0, 1.0, 1.0, 1.0};\n\tauto graphics = std::make_shared<robot_dart::gui::magnum::Graphics>(configuration);\n\tsimu.set_graphics(graphics);\n\tgraphics->look_at({0., 3.5, 2.}, {0., 0., 0.25});\n\tgraphics->record_video("talos_dancing.mp4");\n\t```', 'SET_COLLISION_DETECTOR': '\t```cpp\n\tsimu.set_collision_detector("fcl"); // collision_detector can be "dart", "fcl", "ode" or "bullet" (case does not matter)\n\t```', 'SELF_COLLISIONS': '\t```cpp\n\tif (!robot->self_colliding()) {\n\t    std::cout << "Self collision is not enabled" << std::endl;\n\t    // set self collisions to true and adjacent collisions to false\n\t    robot->set_self_collision(true, false);\n\t}\n\t```', 'FRANKA': '\t```cpp\n\t    auto robot = std::make_shared<robot_dart::robots::Franka>();\n\t    robot->set_actuator_types("torque");\n\t\n\t    // add a PD-controller to the arm\n\t    // set desired positions\n\t    Eigen::VectorXd ctrl = robot_dart::make_vector({0., M_PI / 4., 0., -M_PI / 4., 0., M_PI / 2., 0., 0.});\n\t\n\t    // add the controller to the robot\n\t    auto controller = std::make_shared<robot_dart::control::PDControl>(ctrl);\n\t    robot->add_controller(controller);\n\t    controller->set_pd(300., 50.);\n\t\n\t    // choose time step of 0.001 seconds\n\t    robot_dart::RobotDARTSimu simu(0.001);\n\t    simu.set_collision_detector("fcl");\n\t    simu.enable_status_bar(true, 20); // change the font size\n\t\n\t#ifdef GRAPHIC\n\t    auto graphics = std::make_shared<robot_dart::gui::magnum::Graphics>();\n\t    simu.set_graphics(graphics);\n\t    // set the camera at position (0, 3, 1) looking at the center (0, 0, 0)\n\t    graphics->look_at({0., 3., 1.}, {0., 0., 0.});\n\t#endif\n\t\n\t    simu.add_checkerboard_floor();\n\t    simu.add_robot(robot);\n\t\n\t    simu.run(30.);\n\t    robot.reset();\n\t```', 'ROBOT_POOL_INCLUDE': '\t```cpp\n\t#include <robot_dart/robot_pool.hpp>\n\t```', 'ROBOT_POOL_GLOBAL_NAMESPACE': '\t```cpp\n\tnamespace pool {\n\t    // This function should load one robot: here we load Talos\n\t    inline std::shared_ptr<robot_dart::Robot> robot_creator()\n\t    {\n\t        return std::make_shared<robot_dart::robots::Talos>();\n\t    }\n\t\n\t    // To create the object we need to pass the robot_creator function and the number of maximum parallel threads\n\t    robot_dart::RobotPool robot_pool(robot_creator, NUM_THREADS);\n\t} // namespace pool\n\t```', 'ROBOT_POOL_EVAL': '\t```cpp\n\tinline void eval_robot(int i)\n\t{\n\t    // We get one available robot\n\t    auto robot = pool::robot_pool.get_robot();\n\t    std::cout << "Robot " << i << " got [" << robot->skeleton() << "]" << std::endl;\n\t\n\t    /// --- some robot_dart code ---\n\t    simulate_robot(robot);\n\t    // --- do something with the result\n\t\n\t    std::cout << "End of simulation " << i << std::endl;\n\t\n\t    // CRITICAL : free your robot !\n\t    pool::robot_pool.free_robot(robot);\n\t\n\t    std::cout << "Robot " << i << " freed!" << std::endl;\n\t}\n\t```', 'ROBOT_POOL_CREATE_THREADS': '\t```cpp\n\t// for the example, we run NUM_THREADS threads of eval_robot()\n\tstd::vector<std::thread> threads(NUM_THREADS * 2); // *2 to see some reuse\n\tfor (size_t i = 0; i < threads.size(); ++i)\n\t    threads[i] = std::thread(eval_robot, i); // eval_robot is the function that uses the robot\n\t```', 'TORQUE_SENSOR': '\t```cpp\n\t// Add torque sensors to the robot\n\tint ct = 0;\n\tstd::vector<std::shared_ptr<robot_dart::sensor::Torque>> tq_sensors(robot->num_dofs());\n\tfor (const auto& joint : robot->dof_names())\n\t    tq_sensors[ct++] = simu.add_sensor<robot_dart::sensor::Torque>(robot, joint, 1000);\n\t```', 'FORCE_TORQUE_SENSOR': '\t```cpp\n\t// Add force-torque sensors to the robot\n\tct = 0;\n\tstd::vector<std::shared_ptr<robot_dart::sensor::ForceTorque>> f_tq_sensors(robot->num_dofs());\n\tfor (const auto& joint : robot->dof_names())\n\t    f_tq_sensors[ct++] = simu.add_sensor<robot_dart::sensor::ForceTorque>(robot, joint, 1000, "parent_to_child");\n\t```', 'IMU_SENSOR': '\t```cpp\n\t// Add IMU sensors to the robot\n\tct = 0;\n\tstd::vector<std::shared_ptr<robot_dart::sensor::IMU>> imu_sensors(robot->num_bodies());\n\tfor (const auto& body_node : robot->body_names()) {\n\t    // _imu(std::make_shared<sensor::IMU>(sensor::IMUConfig(body_node("head"), frequency))),\n\t    imu_sensors[ct++] = simu.add_sensor<robot_dart::sensor::IMU>(robot_dart::sensor::IMUConfig(robot->body_node(body_node), 1000));\n\t}\n\t```', 'TORQUE_MEASUREMENT': '\t```cpp\n\t// vector that contains the torque measurement for every joint (scalar)\n\tEigen::VectorXd torques_measure(robot->num_dofs());\n\tfor (const auto& tq_sens : tq_sensors)\n\t    torques_measure.block<1, 1>(ct++, 0) = tq_sens->torques();\n\t```', 'FORCE_TORQUE_MEASUREMENT': '\t```cpp\n\t//  matrix that contains the torque measurement for every joint (3d vector)\n\tEigen::MatrixXd ft_torques_measure(robot->num_dofs(), 3);\n\t//  matrix that contains the force measurement for every joint (3d vector)\n\tEigen::MatrixXd ft_forces_measure(robot->num_dofs(), 3);\n\t//  matrix that contains the wrench measurement for every joint (6d vector)[torque, force]\n\tEigen::MatrixXd ft_wrench_measure(robot->num_dofs(), 6);\n\tct = 0;\n\tfor (const auto& f_tq_sens : f_tq_sensors) {\n\t    ft_torques_measure.block<1, 3>(ct, 0) = f_tq_sens->torque();\n\t    ft_forces_measure.block<1, 3>(ct, 0) = f_tq_sens->force();\n\t    ft_wrench_measure.block<1, 6>(ct, 0) = f_tq_sens->wrench();\n\t    ct++;\n\t}\n\t```', 'IMU_MEASUREMENT': '\t```cpp\n\tEigen::MatrixXd imu_angular_positions_measure(robot->num_bodies(), 3);\n\tEigen::MatrixXd imu_angular_velocities_measure(robot->num_bodies(), 3);\n\tEigen::MatrixXd imu_linear_acceleration_measure(robot->num_bodies(), 3);\n\tct = 0;\n\tfor (const auto& imu_sens : imu_sensors) {\n\t    imu_angular_positions_measure.block<1, 3>(ct, 0) = imu_sens->angular_position_vec();\n\t    imu_angular_velocities_measure.block<1, 3>(ct, 0) = imu_sens->angular_velocity();\n\t    imu_linear_acceleration_measure.block<1, 3>(ct, 0) = imu_sens->linear_acceleration();\n\t    ct++;\n\t}\n\t```', 'RGB_SENSOR': '\t```cpp\n\t// a nested std::vector (w*h*3) of the last image taken can be retrieved\n\tauto rgb_image = camera->image();\n\t```', 'RGB_SENSOR_MEASURE': '\t```cpp\n\t// we can also save them to png\n\trobot_dart::gui::save_png_image("camera-small.png", rgb_image);\n\t// convert an rgb image to grayscale (useful in some cases)\n\tauto gray_image = robot_dart::gui::convert_rgb_to_grayscale(rgb_image);\n\trobot_dart::gui::save_png_image("camera-gray.png", gray_image);\n\t```', 'RGB_D_SENSOR': '\t```cpp\n\t// get the depth image from a camera\n\t// with a version for visualization or bigger differences in the output\n\tauto rgb_d_image = camera->depth_image();\n\t// and the raw values that can be used along with the camera parameters to transform the image to point-cloud\n\tauto rgb_d_image_raw = camera->raw_depth_image();\n\t```', 'RGB_D_SENSOR_MEASURE': '\t```cpp\n\trobot_dart::gui::save_png_image("camera-depth.png", rgb_d_image);\n\trobot_dart::gui::save_png_image("camera-depth-raw.png", rgb_d_image_raw);\n\t```', 'ROBOT_GHOST': '\t```cpp\n\t// Add a ghost robot; only visuals, no dynamics, no collision\n\tauto ghost = robot->clone_ghost();\n\tsimu.add_robot(ghost);\n\t```', 'ADD_NEW_CAMERA': '\t```cpp\n\t// Add camera\n\tauto camera = std::make_shared<robot_dart::sensor::Camera>(graphics->magnum_app(), 256, 256);\n\t```', 'MANIPULATE_CAM_SEP': '\t```cpp\n\tcamera->camera().set_far_plane(5.f);\n\tcamera->camera().set_near_plane(0.01f);\n\tcamera->camera().set_fov(60.0f);\n\t```', 'MANIPULATE_CAM': '\t```cpp\n\tcamera->camera().set_camera_params(5., // far plane\n\t    0.01f, // near plane\n\t    60.0f, // field of view\n\t    600, // width\n\t    400 // height\n\t);\n\t```', 'CAM_POSITION': '\t```cpp\n\t// set the position of the camera, and the position where the main camera is looking at\n\tEigen::Vector3d cam_pos = {-0.5, -3., 0.75};\n\tEigen::Vector3d cam_looks_at = {0.5, 0., 0.2};\n\tcamera->look_at(cam_pos, cam_looks_at);\n\t```', 'CAM_ATTACH': '\t```cpp\n\tEigen::Isometry3d tf;\n\ttf = Eigen::AngleAxisd(3.14, Eigen::Vector3d{1., 0., 0.});\n\ttf *= Eigen::AngleAxisd(1.57, Eigen::Vector3d{0., 0., 1.});\n\ttf.translation() = Eigen::Vector3d(0., 0., 0.1);\n\tcamera->attach_to_body(robot->body_node("iiwa_link_ee"), tf); // cameras are looking towards -z by default\n\t```', 'HELLO_WORLD_INCLUDE': '\t```cpp\n\t#include <robot_dart/robot_dart_simu.hpp>\n\t\n\t#ifdef GRAPHIC\n\t#include <robot_dart/gui/magnum/graphics.hpp>\n\t#endif\n\t```', 'HELLO_WORLD_ROBOT_CREATION': '\t```cpp\n\tauto robot = std::make_shared<robot_dart::Robot>("pexod.urdf");\n\t```', 'HELLO_WORLD_ROBOT_PLACING': '\t```cpp\n\trobot->set_base_pose(robot_dart::make_tf({0., 0., 0.2}));\n\t```', 'HELLO_WORLD_ROBOT_SIMU': '\t```cpp\n\trobot_dart::RobotDARTSimu simu(0.001); // dt=0.001, 1KHz simulation\n\tsimu.add_floor();\n\tsimu.add_robot(robot);\n\t```', 'HELLO_WORLD_ROBOT_GRAPHIC': '\t```cpp\n\t#ifdef GRAPHIC\n\t    auto graphics = std::make_shared<robot_dart::gui::magnum::Graphics>();\n\t    simu.set_graphics(graphics);\n\t    graphics->look_at({0.5, 3., 0.75}, {0.5, 0., 0.2});\n\t#endif\n\t```', 'HELLO_WORLD_ROBOT_RUN': '\t```cpp\n\tsimu.run(10.);\n\t```', 'CAMERAS_PARALLEL': '\t```cpp\n\t// Load robot from URDF\n\tauto global_robot = std::make_shared<robot_dart::robots::Iiwa>();\n\t\n\tstd::vector<std::thread> workers;\n\t\n\t// Set maximum number of parallel GL contexts (this is GPU-dependent)\n\trobot_dart::gui::magnum::GlobalData::instance()->set_max_contexts(4);\n\t\n\t// We want 15 parallel simulations with different GL context each\n\tsize_t N_workers = 15;\n\tstd::mutex mutex;\n\tsize_t id = 0;\n\t// Launch the workers\n\tfor (size_t i = 0; i < N_workers; i++) {\n\t    workers.push_back(std::thread([&] {\n\t        mutex.lock();\n\t        size_t index = id++;\n\t        mutex.unlock();\n\t\n\t        // Get the GL context -- this is a blocking call\n\t        // will wait until one GL context is available\n\t        // get_gl_context(gl_context); // this call will not sleep between failed queries\n\t        get_gl_context_with_sleep(gl_context, 20); // this call will sleep 20ms between each failed query\n\t\n\t        // Do the simulation\n\t        auto robot = global_robot->clone();\n\t\n\t        robot_dart::RobotDARTSimu simu(0.001);\n\t\n\t        Eigen::VectorXd ctrl = robot_dart::make_vector({0., M_PI / 3., 0., -M_PI / 4., 0., 0., 0.});\n\t\n\t        auto controller = std::make_shared<robot_dart::control::PDControl>(ctrl);\n\t        robot->add_controller(controller);\n\t        controller->set_pd(300., 50.);\n\t\n\t        // Magnum graphics\n\t        robot_dart::gui::magnum::GraphicsConfiguration configuration = robot_dart::gui::magnum::WindowlessGraphics::default_configuration();\n\t\n\t        configuration.width = 1024;\n\t        configuration.height = 768;\n\t        auto graphics = std::make_shared<robot_dart::gui::magnum::WindowlessGraphics>(configuration);\n\t        simu.set_graphics(graphics);\n\t        // Position the camera differently for each thread to visualize the difference\n\t        graphics->look_at({0.4 * index, 3.5 - index * 0.1, 2.}, {0., 0., 0.25});\n\t        // record images from main camera/graphics\n\t        // graphics->set_recording(true); // WindowlessGLApplication records images by default\n\t\n\t        simu.add_robot(robot);\n\t        simu.run(6);\n\t\n\t        // Save the image for verification\n\t        robot_dart::gui::save_png_image("camera_" + std::to_string(index) + ".png",\n\t            graphics->image());\n\t\n\t        // Release the GL context for another thread to use\n\t        release_gl_context(gl_context);\n\t    }));\n\t}\n\t\n\t// Wait for all the workers\n\tfor (size_t i = 0; i < workers.size(); i++) {\n\t    workers[i].join();\n\t}\n\t```', 'SET_ACTUATOR': '\t```cpp\n\t// Set all DoFs to same actuator\n\trobot->set_actuator_types("servo"); // actuator types can be "servo", "torque", "velocity", "passive", "locked", "mimic"\n\t// You can also set actuator types separately\n\trobot->set_actuator_type("torque", "iiwa_joint_5");\n\t```', 'POSITIONS_ENFORCED': '\t```cpp\n\t// Εnforce joint position and velocity limits\n\trobot->set_position_enforced(true);\n\t```', 'MODIFY_LIMITS': '\t```cpp\n\t// Modify Position Limits\n\tEigen::VectorXd pos_upper_lims(7);\n\tpos_upper_lims << 2.096, 2.096, 2.096, 2.096, 2.096, 2.096, 2.096;\n\trobot->set_position_upper_limits(pos_upper_lims, dof_names);\n\trobot->set_position_lower_limits(-pos_upper_lims, dof_names);\n\t\n\t// Modify Velocity Limits\n\t\n\tEigen::VectorXd vel_upper_lims(7);\n\tvel_upper_lims << 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5;\n\trobot->set_velocity_upper_limits(vel_upper_lims, dof_names);\n\trobot->set_velocity_lower_limits(-vel_upper_lims, dof_names);\n\t\n\t// Modify Force Limits\n\t\n\tEigen::VectorXd force_upper_lims(7);\n\tforce_upper_lims << 150, 150, 150, 150, 150, 150, 150;\n\trobot->set_force_upper_limits(force_upper_lims, dof_names);\n\trobot->set_force_lower_limits(-force_upper_lims, dof_names);\n\t\n\t// Modify Acceleration Limits\n\tEigen::VectorXd acc_upper_lims(7);\n\tacc_upper_lims << 1500, 1500, 1500, 1500, 1500, 1500, 1500;\n\trobot->set_acceleration_upper_limits(acc_upper_lims, dof_names);\n\trobot->set_acceleration_lower_limits(-acc_upper_lims, dof_names);\n\t```', 'MODIFY_COEFFS': '\t```cpp\n\t// Modify Damping Coefficients\n\tstd::vector<double> damps = {0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4};\n\trobot->set_damping_coeffs(damps, dof_names);\n\t\n\t// Modify Coulomb Frictions\n\tstd::vector<double> cfrictions = {0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001};\n\trobot->set_coulomb_coeffs(cfrictions, dof_names);\n\t\n\t// Modify  Spring Stiffness\n\tstd::vector<double> stiffnesses = {0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001};\n\trobot->set_spring_stiffnesses(stiffnesses, dof_names);\n\t```', 'KINEMATICS': '\t```cpp\n\t// Get Joint Positions(Angles)\n\tauto joint_positions = robot->positions();\n\t\n\t// Get Joint Velocities\n\tauto joint_vels = robot->velocities();\n\t\n\t// Get Joint Accelerations\n\tauto joint_accs = robot->accelerations();\n\t\n\t// Get link_name(str) Transformation matrix with respect to the world frame.\n\tauto eef_tf = robot->body_pose(link_name);\n\t\n\t// Get translation vector from transformation matrix\n\tauto eef_pos = eef_tf.translation();\n\t\n\t// Get rotation matrix from tranformation matrix\n\tauto eef_rot = eef_tf.rotation();\n\t\n\t// Get link_name 6d pose vector [logmap(eef_tf.linear()), eef_tf.translation()]\n\tauto eef_pose_vec = robot->body_pose_vec(link_name);\n\t\n\t// Get link_name 6d velocity vector [angular, cartesian]\n\tauto eef_vel = robot->body_velocity(link_name);\n\t\n\t// Get link_name 6d acceleration vector [angular, cartesian]\n\tauto eef_acc = robot->body_acceleration(link_name);\n\t\n\t// Jacobian targeting the origin of link_name(str)\n\tauto jacobian = robot->jacobian(link_name);\n\t\n\t// Jacobian time derivative\n\tauto jacobian_deriv = robot->jacobian_deriv(link_name);\n\t\n\t// Center of Mass Jacobian\n\tauto com_jacobian = robot->com_jacobian(robot->dof_names());\n\t\n\t// Center of Mass Jacobian Time Derivative\n\tauto com_jacobian_deriv = robot->com_jacobian_deriv(robot->dof_names());\n\t```', 'DYNAMICS': "\t```cpp\n\t// Get Joint Forces\n\tauto joint_forces = robot->forces();\n\t\n\t// Get link's mass\n\tauto eef_mass = robot->body_mass(link_name);\n\t\n\t// Mass Matrix of robot\n\tauto mass_matrix = robot->mass_matrix();\n\t\n\t// Inverse of Mass Matrix\n\tauto inv_mass_matrix = robot->inv_mass_matrix();\n\t\n\t// Augmented Mass matrix\n\tauto aug_mass_matrix = robot->aug_mass_matrix();\n\t\n\t// Inverse of Augmented Mass matrix\n\tauto inv_aug_mass_matrix = robot->inv_aug_mass_matrix();\n\t\n\t// Coriolis Force vector\n\tauto coriolis = robot->coriolis_forces();\n\t\n\t// Gravity Force vector\n\tauto gravity = robot->gravity_forces();\n\t\n\t// Combined vector of Coriolis Force and Gravity Force\n\tauto coriolis_gravity = robot->coriolis_gravity_forces();\n\t\n\t// Constraint Force Vector\n\tauto constraint_forces = robot->constraint_forces(robot->dof_names());\n\t```"}
    for v in variables.items():
        env.variables[v[0]] = variables[v[0]]
