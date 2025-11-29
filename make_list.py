#python make_list.py ^
 # "E:\Resound Project\buriy_audiobooks_2_val.tar\buriy_audiobooks_2_val" ^
 # "E:\Resound Project\buriy_train.list"

import os
import argparse

def collect_pairs(root_dir):
    """
    Ищем все .wav и к каждому пытаемся найти .txt с тем же именем.
    Возвращаем список кортежей: (wav_path, speaker_name, text).
    """
    pairs = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Список wav в текущей директории
        wav_files = [f for f in filenames if f.lower().endswith(".wav")]

        # Для каждого wav ищем .txt с тем же именем
        for wav in wav_files:
            base = os.path.splitext(wav)[0]  # 1544b79cf3ff
            txt = base + ".txt"
            wav_path = os.path.join(dirpath, wav)
            txt_path = os.path.join(dirpath, txt)

            if not os.path.isfile(txt_path):
                # Если нет текста — можно пропустить или залогировать
                print(f"[WARN] Нет txt для {wav_path}")
                continue

            # Читаем текст (предполагаю UTF-8, можно поменять при необходимости)
            with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read().strip()

            # На всякий случай заменим переносы строк на пробел
            text = " ".join(text.splitlines()).strip()

            speaker_name = base  # как в примере

            pairs.append((wav_path, speaker_name, text))

    return pairs


def main():
    parser = argparse.ArgumentParser(
        description="Сбор аннотаций для GPT-SoVITS: wav|speaker|ru|text"
    )
    parser.add_argument(
        "root_dir",
        help="Корневая директория с аудио и текстами "
             "(например: E:\\Resound Project\\buriy_audiobooks_2_val.tar\\buriy_audiobooks_2_val)",
    )
    parser.add_argument(
        "out_list",
        help="Путь к выходному .list файлу (например: buriy_train.list)",
    )
    parser.add_argument(
        "--language",
        default="ru",
        help="Код языка (по умолчанию ru)",
    )

    args = parser.parse_args()

    root_dir = args.root_dir
    out_list = args.out_list
    lang = args.language

    pairs = collect_pairs(root_dir)
    print(f"[INFO] Найдено пар wav+txt: {len(pairs)}")

    with open(out_list, "w", encoding="utf-8") as out_f:
        for wav_path, speaker, text in pairs:
            # Нормализуем путь к Windows-формату с обратными слэшами
            norm_path = os.path.normpath(wav_path)
            # Оборачиваем путь в кавычки, как ты просил
            line = f"\"{norm_path}\"|{speaker}|{lang}|{text}\n"
            out_f.write(line)

    print(f"[INFO] Готово. Сохранено в {out_list}")


if __name__ == "__main__":
    main()
