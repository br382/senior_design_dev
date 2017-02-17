%% Plotting Experimental Data Set
close all;
clear all;
clc;
fig = 0;

files = {'data_take2.csv'}; %or {} or {file0.csv, file1.csv... etc.}
files = {};
if length(files) <= 0
    files = uigetfile('*.csv','Select Data Set(s)','MultiSelect','on');
end
if ~iscell(files) %force into iterable, if only 1 input file.
    files = {files};
end

for i = 1:length(files)
    col_data   = csvread(files{i}, 1);
    time_mills = col_data(:,1);
    titles = {'Time (ms)'; ...
        'Active Hopper'; 'Active Tank'; 'Passive Hopper'}; %, 'Passive Tank'};
    clear data;
    for j=2:min(size(col_data))
        bits_threshold = 50;
        data_ind       = find(col_data(:,j) < bits_threshold);
        time_threshold = 100;
        data_ind_ind   = min(find(data_ind > time_threshold));
        time_ms        = time_mills(data_ind(data_ind_ind));
        time_done      = double(time_ms)/1000.0;
        time_done      = time_done / 3600.0;
        fprintf('%s Runtime: %.3f Hours, (msec %d)\n', titles{j}, time_done, time_ms);
    end
    colors = hsv(min(size(col_data)));
    for j = 1:min(size(col_data))
        if j <= length(titles)
            data{j}.title = titles{j};
        else
            data{j}.title = sprintf('Input %.0d', j);
        end
        %data{j}.title = sprintf('Input %.0d', j);
        data{j}.y     = col_data(:,j);
        data{j}.x     = time_mills;
        % don't plot TIME vs TIME.
        if j ~= 0 %usually 1, debug 0
            fig = fig+1;
            figure('units','normalized','outerposition',[0 0 1 1]);
            plot(  data{j}.x, data{j}.y, 'color', colors(j,:));
            ylabel( data{j}.title);
            xlabel(titles(1));
            title(sprintf('Data Set %.0d: %s', i, data{j}.title));
        end
        %%
    end
    %%
    fig = fig+1;
    figure('units','normalized','outerposition',[0 0 1 1]);
    hold on;
    for j = 2:length(data)
        plot(data{j}.x, data{j}.y, 'Color', colors(j,:));
    end
    ylabel('A/D Magnitude in Bits'  );
    xlabel('Time in milliseconds'   );
    legend(titles(2:length(titles)) );
    title(sprintf('Data Set %.0d: %s', i, 'All Analog Inputs Plot') );
    hold off;
    %%
    fig = fig+1;
    figure('units','normalized','outerposition',[0 0 1 1]);
    hold on;
    for j = 2:length(data)
        plot(data{j}.x, data{j}.y, '.', 'Color', colors(j,:));
    end
    ylabel('A/D Magnitude in Bits'  );
    xlabel('Time in milliseconds'   );
    legend(titles(2:length(titles)) );
    title(sprintf('Data Set %.0d: %s', i, 'All Analog Inputs Plot') );
    hold off;
    %%
    fit = polyfit(transpose(time_mills), 1:length(time_mills),1);
    avg_period = 1/fit(1);
    fprintf('\nData Set %s (%.0d) ', files{i}, i);
    fprintf('has an Average Sampling Rate of %.3f ', avg_period);
    fprintf('milliseconds.\n');
    %%
    fs_rate   = 1000/(avg_period); %ms to Hz
    N_samples = length(time_mills);
    f_axis    = linspace(-fs_rate/2,fs_rate/2,N_samples);
    % dft with length N, from frequency [-fs/2:fs/2], divided over N bins.
    clear data;
    for j = 1:min(size(col_data))
        if j <= length(titles)
            data{j}.title = titles{j};
        else
            data{j}.title = sprintf('Input %.0d', j);
        end
        data{j}.title = sprintf('FFT of %s', data{j}.title);
        data{j}.y = col_data(:,j);
        %fixing bad Arduino conversion factors... from first run.
        if mean(data{j}.y) < 5
            data{j}.y = data{j}.y .* 1023.0 ./ 5.0;%return volts to bits.
        end
        data{j}.y     = fftshift(fft(data{j}.y));
        data{j}.x     = f_axis;
        % don't plot TIME vs TIME.
        if j ~= 0 %usually 1, debug 0
            fig = fig+1;
            figure(fig, 'units','normalized','outerposition',[0 0 1 1]);
            semilogy(  data{j}.x, abs(data{j}.y), 'color', colors(j,:));
            ylabel( data{j}.title);
            xlabel('Frequency in Hz');
            title(sprintf('Data Set %.0d: %s', i, data{j}.title));
        end
        %%
    end
    %%
    fig = fig+1;
    figure('units','normalized','outerposition',[0 0 1 1]);
    hold on;
    for j = 2:length(data)
        semilogy(data{j}.x, abs(data{j}.y), 'Color', colors(j,:));
    end
    ylabel('A/D Magnitude in Bits'  );
    xlabel('Frequency in Hz'        );
    legend(titles(2:length(titles)) );
    title(sprintf('Data Set %.0d: %s', i, 'All Analog Inputs Plot') );
    set(gca, 'yscale','log');
    hold off;
    %%
    fig = fig+1;
    figure('units','normalized','outerposition',[0 0 1 1]);
    hold on;
    for j = 2:length(data)
        semilogy(data{j}.x, abs(data{j}.y), '.', 'Color', colors(j,:));
    end
    ylabel('A/D Magnitude in Bits'  );
    xlabel('Frequency in Hz'        );
    legend(titles(2:length(titles)) );
    title(sprintf('Data Set %.0d: %s', i, 'All Analog Inputs Plot') );
    set(gca, 'yscale','log');
    hold off;
    %%
end