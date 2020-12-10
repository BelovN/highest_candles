import os
import xlwt
from xlwt import Workbook
from settings import OUTPUT_DIR


style = xlwt.easyxf('font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white;')

style_all_green = xlwt.easyxf('font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color lime; \
                     align: horiz center')

style_center = xlwt.easyxf('font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white;\
                     align: horiz center')



def write_full_statistic_to_excel(statistic, meta_statistic):
    wb = Workbook()
    metastatistic_to_excel(meta_statistic, wb)
    statistic_to_excel(statistic, wb)
    wb.save(os.path.join(OUTPUT_DIR, 'statistic.xls'))


def metastatistic_to_excel(meta_statistic, wb):
    sheet = wb.add_sheet('Общая информация', cell_overwrite_ok=True)
    sheet.write_merge(0, 1, 0, 0, 'Логика - Краткое описание', style=style)
    sheet.write_merge(0, 1, 1, 3, 'Открываем сделку на пробой максимума или минимума', style=style_center)

    sheet.write(2, 0, 'Управление капиталом', style=style)
    sheet.write(2, 1, meta_statistic['start_capital'], style=style_center)
    sheet.write(2, 2, 'Фиксированный процент:', style=style_center)
    sheet.write(2, 3, meta_statistic['fixed_percent'], style=style_center)

    sheet.write(3, 0, 'Инструмент и таймфрейм', style=style)
    sheet.write_merge(3, 3, 1, 3, meta_statistic['filename'], style=style_center)

    sheet.write(4, 0, 'Тестируемое окно истории', style=style)
    sheet.write(4, 1, meta_statistic['date_start'], style=style)
    sheet.write(4, 2, meta_statistic['date_finish'], style=style)

    sheet.write(5, 0, 'Полученный капитал', style=style)
    sheet.write_merge(5, 5, 1, 3, meta_statistic['start_capital'] + \
                                    meta_statistic['total'],
                                    style=style_center)

    sheet.write(6, 1, 'Всего', style=style_all_green)
    sheet.write(6, 2, 'LONG', style=style_all_green)
    sheet.write(6, 3, 'SHORT', style=style_all_green)

    sheet.write(7, 0, 'Кол-во сделок', style=style)
    sheet.write(7, 1, meta_statistic['count_all'], style=style)
    sheet.write(7, 2, meta_statistic['count_long'], style=style)
    sheet.write(7, 3, meta_statistic['count_short'], style=style)

    sheet.write(8, 0, 'Средний П/У', style=style)
    sheet.write(8, 1, meta_statistic['avr_profit'] - abs(meta_statistic['avr_lesion']), style=style)
    sheet.write(8, 2, meta_statistic['avr_profit_long'] - abs(meta_statistic['avr_lesion_long']), style=style)
    sheet.write(8, 3, meta_statistic['avr_profit_short'] - abs(meta_statistic['avr_lesion_short']), style=style)

    sheet.write(9, 0, 'Средний П/У %', style=style)
    sheet.write(9, 1, meta_statistic['P/L'], style=style)
    sheet.write(9, 2, meta_statistic['(P/L)_long'], style=style)
    sheet.write(9, 3, meta_statistic['(P/L)_short'], style=style)

    sheet.write(10, 0, 'Баров на сделку (в среднем)', style=style)
    sheet.write(10, 1, meta_statistic['count_bars'], style=style)
    sheet.write(10, 2, meta_statistic['count_bars_long'], style=style)
    sheet.write(10, 3, meta_statistic['count_bars_short'], style=style)

    sheet.write(11, 0, 'Общий П/У', style=style)
    sheet.write(11, 1, meta_statistic['sum_profit'] - abs(meta_statistic['sum_lesion']), style=style)
    sheet.write(11, 2, meta_statistic['sum_profit_long'] - abs(meta_statistic['sum_lesion_long']), style=style)
    sheet.write(11, 3, meta_statistic['sum_profit_short'] - abs(meta_statistic['sum_lesion_short']), style=style)

    sheet.write(13, 0, 'Выиграно сделок', style=style)
    sheet.write(13, 1, meta_statistic['count_profit'], style=style)
    sheet.write(13, 2, meta_statistic['count_profit_long'], style=style)
    sheet.write(13, 3, meta_statistic['count_profit_short'], style=style)

    sheet.write(14, 0, 'Выиграно %', style=style)
    sheet.write(14, 1, (meta_statistic['count_profit']/meta_statistic['count_all'])*100, style=style)
    sheet.write(14, 2, (meta_statistic['count_profit_long']/meta_statistic['count_all'])*100, style=style)
    sheet.write(14, 3, (meta_statistic['count_profit_short']/meta_statistic['count_all'])*100, style=style)

    sheet.write(15, 0, 'Общая прибыль', style=style)
    sheet.write(15, 1, meta_statistic['total'], style=style)
    sheet.write(15, 2, meta_statistic['total_long'], style=style)
    sheet.write(15, 3, meta_statistic['total_short'], style=style)

    sheet.write(16, 0, 'Средняя прибыль', style=style)
    sheet.write(16, 1, meta_statistic['avr_profit'], style=style)
    sheet.write(16, 2, meta_statistic['avr_profit_long'], style=style)
    sheet.write(16, 3, meta_statistic['avr_profit_short'], style=style)

    sheet.write(17, 0, 'Средняя прибыль %', style=style)
    sheet.write(17, 1, (meta_statistic['avr_profit']/meta_statistic['start_capital'])*100, style=style)
    sheet.write(17, 2, (meta_statistic['avr_profit_long']/meta_statistic['start_capital'])*100, style=style)
    sheet.write(17, 3, (meta_statistic['avr_profit_short']/meta_statistic['start_capital'])*100, style=style)

    sheet.write(18, 0, 'Максимум подряд выигрышных', style=style)
    sheet.write(18, 1, meta_statistic['count_profit_row'], style=style)
    sheet.write(18, 2, meta_statistic['count_profit_row_long'], style=style)
    sheet.write(18, 3, meta_statistic['count_profit_row_short'], style=style)

    sheet.write(20, 0, 'Убыточных сделок', style=style)
    sheet.write(20, 1, meta_statistic['count_lesion'], style=style)
    sheet.write(20, 2, meta_statistic['count_lesion_long'], style=style)
    sheet.write(20, 3, meta_statistic['count_lesion_short'], style=style)

    sheet.write(21, 0, 'Убыточно %', style=style)
    sheet.write(21, 1, abs(meta_statistic['sum_lesion']/meta_statistic['start_capital'])*100, style=style)
    sheet.write(21, 2, abs(meta_statistic['sum_lesion_long']/meta_statistic['start_capital'])*100, style=style)
    sheet.write(21, 3, abs(meta_statistic['sum_lesion_short']/meta_statistic['start_capital'])*100, style=style)

    sheet.write(22, 0, 'Общий убыток', style=style)
    sheet.write(22, 1, abs(meta_statistic['sum_lesion']), style=style)
    sheet.write(22, 2, abs(meta_statistic['sum_lesion_long']), style=style)
    sheet.write(22, 3, abs(meta_statistic['sum_lesion_short']), style=style)

    sheet.write(23, 0, 'Средний убыток', style=style)
    sheet.write(23, 1, abs(meta_statistic['avr_lesion']), style=style)
    sheet.write(23, 2, abs(meta_statistic['avr_lesion_long']), style=style)
    sheet.write(23, 3, abs(meta_statistic['avr_lesion_short']), style=style)

    sheet.write(24, 0, 'Средний убыток %', style=style)
    sheet.write(24, 1, abs(meta_statistic['avr_lesion']/meta_statistic['start_capital'])*100, style=style)
    sheet.write(24, 2, abs(meta_statistic['avr_lesion_long']/meta_statistic['start_capital'])*100, style=style)
    sheet.write(24, 3, abs(meta_statistic['avr_lesion_short']/meta_statistic['start_capital'])*100, style=style)

    sheet.write(25, 0, 'Максимум подряд убыточных', style=style)
    sheet.write(25, 1, meta_statistic['count_lesion_row'], style=style)
    sheet.write(25, 2, meta_statistic['count_lesion_row_long'], style=style)
    sheet.write(25, 3, meta_statistic['count_lesion_row_short'], style=style)

    sheet.write(27, 0, 'Максимальная просадка', style=style)
    sheet.write(27, 1, abs(meta_statistic['worst_lesion']), style=style)
    sheet.write(27, 2, '', style=style)
    sheet.write(27, 3, '', style=style)

    sheet.write(28, 0, 'День макс.просадки', style=style)
    sheet.write(28, 1, meta_statistic['worst_day'], style=style)
    sheet.write(28, 2, '', style=style)
    sheet.write(28, 3, '', style=style)

    sheet.write(30, 0, 'Профит фактор', style=style)
    sheet.write(30, 1, meta_statistic['avr_profit'] / meta_statistic['avr_lesion'], style=style)

    if meta_statistic['avr_lesion_long'] != 0:
        sheet.write(30, 2, meta_statistic['avr_profit_long'] / meta_statistic['avr_lesion_long'], style=style)
    else:
        sheet.write(30, 2, 0, style=style)


    if meta_statistic['avr_lesion_short'] != 0:
        sheet.write(30, 3, meta_statistic['avr_profit_short'] / meta_statistic['avr_lesion_short'], style=style)
    else:
        sheet.write(30, 3, 0, style=style)

    sheet.write(31, 0, 'Фактор восстановления', style=style)
    sheet.write(31, 1, meta_statistic['total'] / meta_statistic['worst_lesion'], style=style)
    sheet.write(31, 2, '', style=style)
    sheet.write(31, 3, '', style=style)

    sheet.write(32, 0, 'Коэф выигрыша', style=style)
    sheet.write(32, 1, meta_statistic['P/L'], style=style)
    sheet.write(32, 2, meta_statistic['(P/L)_long'], style=style)
    sheet.write(32, 3, meta_statistic['(P/L)_short'], style=style)

    for i in range(4):
        col = sheet.col(i)
        col.width = 256 * 28


def statistic_to_excel(statistic, wb):
    sheet = wb.add_sheet('Информация по сделкам')
    HEADERS = [
        'Позиция', 'Причина входа', 'Дата входа', 'Время входа', 'Цена входа',
        'Причина выхода', 'Дата выхода', 'Время выхода', 'Цена выхода',
        'Лоты. Начальные', 'Изменение лотов', 'Причина увеличения',
        'Изменение лотов', 'Причина уменьшения', 'Средневзвешенная цена входа',
        'Средневзвешенная цена выхода', 'П/У сделки', 'П/У суммарно', 'Длина сделки',
        'Кол-во свечей до новой сделки', 'Доход/Свечей', '% Изменения',
        'Максимальная прибыль в моменте', 'Стоп уровень',
    ]
    for i, header in enumerate(HEADERS):
        sheet.write(0, i, header, style=style_center)
        col = sheet.col(i)
        col.width = 256 * (len(header) + 3)

    sum_delta_price = 0
    for i in range(len(statistic['ind_out'])):
        position = 'LONG' if statistic['status'][i] == 1 else 'SHORT'
        sheet.write(i+1, 0, position, style=style_center)
        sheet.write(i+1, 1, 'Входной сигнал', style=style_center)

        date_in, time_in = statistic['time_in'][i].split(' ')
        sheet.write(i+1, 2, date_in, style=style_center)
        sheet.write(i+1, 3, time_in, style=style_center)

        sheet.write(i+1, 4, statistic['point_in'][i], style=style_center)

        sheet.write(i+1, 5, 'Обратный сигнал', style=style_center)

        date_out, time_out = statistic['time_out'][i].split(' ')
        sheet.write(i+1, 6, date_out, style=style_center)
        sheet.write(i+1, 7, time_out, style=style_center)

        sheet.write(i+1, 8, statistic['point_out'][i], style=style_center)
        sheet.write(i+1, 9, statistic['contracts'][i], style=style_center)
        sheet.write(i+1, 10, 'Не проводится', style=style_center)
        sheet.write(i+1, 11, '-', style=style_center)
        sheet.write(i+1, 12, 'Не проводится', style=style_center)
        sheet.write(i+1, 13, '-', style=style_center)
        sheet.write(i+1, 14, '-', style=style_center)
        sheet.write(i+1, 15, '-', style=style_center)

        sum_delta_price += statistic['delta_price'][i]
        sheet.write(i+1, 16, statistic['delta_price'][i], style=style_center)
        sheet.write(i+1, 17, sum_delta_price, style=style_center)

        length_deal = statistic['ind_out'][i] - statistic['ind_in'][i]
        sheet.write(i+1, 18, length_deal, style=style_center)

        if i > 0:
            count_candles_to_new_deal =  statistic['ind_in'][i] - statistic['ind_out'][i-1]
        else:
            count_candles_to_new_deal = ''

        sheet.write(i+1, 19, count_candles_to_new_deal, style=style_center)

        profit_for_candles = statistic['delta_price'][i] / length_deal
        sheet.write(i+1, 20, profit_for_candles, style=style_center)

        percent_change = (statistic['delta_price'][i] / statistic['capital_story'][i]) * 100
        sheet.write(i+1, 21, percent_change, style=style_center)

        sheet.write(i+1, 22, statistic['delta_potencial'][i], style=style_center)

        sheet.write(i+1, 23, statistic['stop_loss'][i], style=style_center)
        # sheet.write(i+1, 23, '-', style=style_center)








def main():
    write_full_statistic_to_excel(123,123)


if __name__ == '__main__':
    main()
