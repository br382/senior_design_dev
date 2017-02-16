%% Data Links Plots
clc;
sensors_per_unit = 1:3;
number_of_units  = 1:100;

link_title = {
    'MCU -> Sensor',
    'Sensor -> Server',
    'HUD -> Server (const)',
    'HUD -> Server (scale)',
    'Pos (HUD GPS) -> Sensor',
    'Node Server -> External Server'
};
link_data_up = [
    148, 735, 18, 18, 220, 18
];
link_data_down = [
    15, 12, 2, 5+735, 17, 735
];
sig_num_title = {
    'Localhost Combined',
    'Node Internal Serial',
    'Node Internal Socket',
    'All External Socket',
    'Total'
};
sig_num = [
    link_data_up(1) + link_data_down(1),
    link_data_up(2) + link_data_down(2),
    link_data_up(3) + link_data_down(3),
    link_data_up(4) + link_data_down(4),
    link_data_up(5) + link_data_down(5)
];

inc = 0;
data = []; num = []; sen = []; sig = [];
fprintf('Length %d\n', length(sensors_per_unit)*length(number_of_units));
for s = sensors_per_unit
    for n = number_of_units
        inc  = inc + 1;
        up   = [link_data_up(1) * s,...
            link_data_up(2:length(link_data_up))];
        down = [link_data_down(1) * s,...
            link_data_down(2:length(link_data_down))];
        link_data_combined = up + down;
        data = [data;link_data_combined];
        num  = [num; n];
        sen  = [sen; s];
        scaled = [link_data_combined(2),
                  link_data_combined(1) * s,
                  link_data_combined(2) + link_data_combined(5) + ...
                    link_data_combined(3) + n*link_data_combined(4),
                  n*(n-1)*link_data_combined(6),
                  link_data_combined(1) * s * n + ...
                    n * (link_data_combined(2) + link_data_combined(5)+...
                    link_data_combined(3) + n*link_data_combined(4) )+...
                    n*(n-1)*link_data_combined(6)
                  ];
        sig  = [sig; scaled'];
    end
end
%%
plot3(num, sen, sig(:,5), '.');
