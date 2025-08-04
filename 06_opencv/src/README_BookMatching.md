## ✅ 프로젝트 목적 및 배경

### 카메라 및 이미지 파일을 활용한 객체 인식

---

## 주요 구성 요소 및 흐름

### 검색 설정 변수
```python
ratio = 0.5
MIN_MATCH = 20
```
- ratio는 좋은 매칭 선별 비율로서 **낮을수록 엄격** 함, 기본 0.5~0.8로 형성함
- MIN_MATCH는 최소 매칭점 갯수로서 **적을수록 관대**함, 기본 5~20을 형성함

### ORB & FLANN 설정
```python
orb = cv2.ORB_create(1000)
index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)
search_params = dict(checks=32)
matcher = cv2.FlannBasedMatcher(index_params, search_params)
```
- ORB로 keypoint 및 descriptor 추출
- keypoint란 영상 프레임에서 객체의 모서리, 엣지, 점이 강하게 변화하는 부분들을 ORB 혹은, 알고리즘이 자동으로 검출한 특징점을 지칭한다 따라서 **1000**이라는 숫자는 **1000개의 keypoint를 추출하도록 설정한 것을 말한다**
- FLANN으로 효율적인 유사점 매칭 수행

### KNN 매칭 및 Lowe’s 비율 테스트
```python
matches = matcher.knnMatch(desc1, desc2, 2)
good_matches = [m[0] for m in matches if len(m) == 2 and m[0].distance < m[1].distance * 0.75]
```
- `knnMatch(..., 2)`는 각 descriptor마다 가장 가까운 2개 후보를 반환
- `0.75`는 **Lowe's 비율 테스트** 기준으로, 매칭의 정확도를 향상시킴

---





