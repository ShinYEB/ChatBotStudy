import os
import math
import fitz  # PyMuPDF 설치 필요: pip install pymupdf
from glob import glob

def split_large_pdfs_in_folder(folder_path, target_size_mb=200):
    # 폴더 내 모든 PDF 파일 찾기
    pdf_files = glob(os.path.join(folder_path, "*.pdf"))
    save_folder = os.path.join(folder_path, "split")
    if not pdf_files:
        print(f"📂 '{folder_path}' 폴더에 PDF 파일이 없습니다.")
        return

    print(f"🔍 총 {len(pdf_files)}개의 파일을 검사합니다...")

    for pdf_path in pdf_files:
        try:
            # 1. 파일 크기 확인 (MB 단위)
            file_size_bytes = os.path.getsize(pdf_path)
            file_size_mb = file_size_bytes / (1024 * 1024)

            # 파일명만 추출 (예: 'manual.pdf')
            filename = os.path.basename(pdf_path)

            # 3. 200MB 초과 시 분할 로직 시작
            print(f"✂️ [Split] {filename} ({file_size_mb:.2f} MB) -> 분할 시작")

            doc = fitz.open(pdf_path)
            total_pages = len(doc)

            # 몇 등분 해야 하는지 계산 (예: 450MB / 200MB = 2.25 -> 올림해서 3등분)
            num_splits = math.ceil(file_size_mb / target_size_mb)

            # 한 파일당 대략적인 페이지 수 계산
            pages_per_split = math.ceil(total_pages / num_splits)

            base_name = os.path.splitext(filename)[0]  # 확장자 제외한 이름

            for i in range(num_splits):
                start_page = i * pages_per_split
                end_page = min((i + 1) * pages_per_split, total_pages)

                if start_page >= end_page:
                    break

                # 새 PDF 생성 및 페이지 복사
                new_doc = fitz.open()
                new_doc.insert_pdf(doc, from_page=start_page, to_page=end_page - 1)

                # 저장 파일명: 원본이름_part1.pdf, 원본이름_part2.pdf ...
                output_filename = f"{base_name}_part{i + 1}.pdf"
                output_path = os.path.join(save_folder, output_filename)

                # garbage=4: 압축 및 미사용 리소스 제거 (용량 최적화)
                new_doc.save(output_path, garbage=4)
                new_doc.close()

                print(f"   -> 저장됨: {output_filename} ({start_page + 1}~{end_page}페이지)")

            doc.close()

            # (선택 사항) 원본 파일 삭제를 원하시면 아래 주석을 해제하세요.
            # os.remove(pdf_path)
            # print(f"   -> 원본 파일 삭제됨: {filename}")

        except Exception as e:
            print(f"❌ 오류 발생 ({pdf_path}): {e}")

    print("\n🎉 모든 작업이 완료되었습니다.")