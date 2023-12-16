from models import select_data
if __name__ == '__main__':
    # посчитать количество всех движений мыши
    query1 = select_data("select count() from antonovao.move_mouse_buffer")
    print(query1)
    # посчитать кол-во движений мыши, попадающих в диапазон x < 1000 AND y < 1000 и сгруппировать по target
    query2 = select_data("select target, count() from antonovao.move_mouse_buffer where x < 1000 AND y < 1000 group by target")
    print(query2)
    # найти наиболее большие движения мыши (можно посчитать с помощью дельт: plus(abs(deltaX), abs(deltaY))
    query3 = select_data("""select a.*, plus(abs(deltaX), abs(deltaY)) move
                            from antonovao.move_mouse_buffer a
                                join (select 
                                        max(plus(abs(deltaX), abs(deltaY))) max_move
                                    from antonovao.move_mouse_buffer) as b
                                on plus(abs(deltaX), abs(deltaY)) = b.max_move""")
    print(query3)