Курс Adalm-Pluto SDR

### task1 - основы, генерация сигнала в реальном времени

### task2 - Формирование сигналов, визуализация в Python. 
    test_list.py - Сравнение скорости работы lists и NumPy

<img src= "task2/test_sort_speed.png">

    test_plot.py - Создание графиков с различным стилем отображения

<img src= "task2/type_plot.png">


### task3 - Изучение основных параметров библиотеки PyAdi для Adalm Pluto SDR


    Определение наисильнейшего сигнала - 2412 Мгц
    Передача данных на данной частоте
<img src= "task3/signal_data.jpg">
<img src= "task3/signal_data_2.jpg">

    Практика
    Практическое занятие по разделу Дискретизация сигналов

        Значение аналоговой частоты сигнала при частоте дискретизации = 1000 отсчетов/c, которая соответствует нормированной частоте Ω=0.4π рад равна 200 Гц

        Временные диаграммы 

<img src= "task3/sampling_rate_1000.png">
<img src= "task3/sampling_rate_1000_fft.png">

        Частота дискретизации 500 отсчетов/с
        Количество отсчетов сигнала порядка 200 в команде arrange

<img src= "task3/arrange_200.png">

        fft

<img src= "task3/arrange_200_fft.png">

### task4 - Изучение основных свойств ДПФ с помощью моделирования в  Python/Spyder
    ds_Fourier.py - дискретное преобразование Фурье
<img src= "task4/ds_fourier.png">
    prtask2.py - Преобразование Фурье к сигналу полученному от Adalm_Pluto_SDR
