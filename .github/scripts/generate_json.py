import os
import json
from datetime import datetime

def is_valid_directory(dir_name):
    """디렉토리 이름이 올바른 형식인지 확인"""
    return '_' in dir_name and os.path.isdir(dir_name) and not dir_name.startswith('.')

def is_valid_image(file_name):
    """이미지 파일이 올바른 형식인지 확인"""
    return file_name.endswith('.png') and '_' in file_name

def get_image_url(repo_owner, dir_name, file_name):
    """GitHub Pages의 이미지 URL 생성"""
    return f"https://{repo_owner}.github.io/baby-flashcard-repo/{dir_name}/{file_name}"

def generate_flashcards_json():
    # GitHub 저장소 소유자 이름 가져오기
    repo_owner = os.environ.get('GITHUB_REPOSITORY_OWNER', 'sb2chun')
    base_path = os.getcwd()  # 현재 작업 디렉토리
    
    data = {
        "lastUpdated": datetime.utcnow().isoformat() + "Z",
        "categories": []
    }
    
    # 모든 디렉토리 순회
    for item in os.listdir(base_path):
        if not is_valid_directory(item):
            continue
            
        # 카테고리 이름 파싱
        kor_name, eng_name = item.split("_")
        category = {
            "path": item,
            "korName": kor_name,
            "engName": eng_name,
            "items": []
        }
        
        # 디렉토리 내 이미지 파일 처리
        category_path = os.path.join(base_path, item)
        for image_file in os.listdir(category_path):
            if not is_valid_image(image_file):
                continue
                
            # 이미지 파일명에서 한글/영문 단어 추출
            file_name_without_ext = image_file.replace(".png", "")
            kor_word, eng_word = file_name_without_ext.split("_")
            
            image_data = {
                "id": f"{item}-{len(category['items']) + 1}",
                "image": get_image_url(repo_owner, item, image_file),
                "kor_word": kor_word,
                "eng_word": eng_word
            }
            category["items"].append(image_data)
        
        # 이미지가 있는 카테고리만 추가
        if category["items"]:
            data["categories"].append(category)
    
    # 결과 JSON 파일 생성
    output_path = os.path.join(base_path, "dist", "flashcards.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"JSON file generated at: {output_path}")
    print(f"Total categories: {len(data['categories'])}")
    print(f"Total items: {sum(len(cat['items']) for cat in data['categories'])}")

if __name__ == "__main__":
    try:
        generate_flashcards_json()
    except Exception as e:
        print(f"Error generating JSON: {str(e)}")
        raise