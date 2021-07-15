# 21_summer_internship
21년도 하계 인턴십 with_vision
<br>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  </head>
  <body>
    <article id="cfb586aa-aa88-48ab-acbf-c0bd53e9f503" class="page sans">
      <header>
        <h1 class="page-title">hrnet 학습 결과</h1>
      </header>
      <div class="page-body">
        <h1 id="4bd45150-08b9-4dfc-96f9-27df0cb3047a" class="">모델학습</h1>
        <p id="f25dc045-ed16-40fb-8234-c509c511bd96" class="">model: hrnet_w32_256x192 사용</p>
        <figure id="8ada5501-0041-40fc-8815-28659543efa2" class="image">
          <a href="image/hrnet.png">
            <img style="width:613px" src="image/hrnet.png" width="50%" height="50%"/>
          </a>
        </figure>
        <p id="4212d0a1-f7f4-4dfa-b795-c85826ede0b5" class="">model1 = test loss : 0.0005 Accuracy : 100</p>
        <p id="9829864e-bdd6-4cd8-b3db-e1b2fb1e9584" class=""></p>
        <h2 id="0362c558-e8a2-4210-88d5-a554d9decd3a" class="">테스트 지표 생성:</h2>
        <p id="76597cf2-c1c1-43b9-9bf7-e2f7686825e3" class="">boundary_size = (top_y – middle_y)/ z 의 값을 기준으로 얼마나 벗어났는가를 판단.</p>
        <figure id="aaa4694e-1781-426e-8efc-a988cd053aae" class="image">
          <a href="image/Untitled.png">
            <img style="width:192px" src="image/Untitled.png" width="30%" height="30%"/>
          </a>
        </figure>
        <p id="5ad8ace8-7803-4686-887d-78a7b81cda61" class="">boundary_size is 10, count of overrange : 0, Accuracy: 100.0%</p>
        <p id="33c599e4-3718-466c-966d-12b26831ac26" class="">boundary_size is 15, count of overrange : 0, Accuracy: 100.0%</p>
        <p id="0de8c74e-96d6-4083-861f-efc4e96b345d" class="">boundary_size is 20, count of overrange : 1, Accuracy: 99.0%</p>
        <p id="116e3ca5-9da6-4186-b798-2931988ee836" class="">boundary_size is 30, count of overrange : 14, Accuracy: 95%</p>
        <p id="928c7f8d-6981-4eec-8ceb-4fa2e9e4c90d" class=""></p>
        <p id="89e85614-98c5-46cd-b28b-c7895f93a828" class="">성능을 개선하기 위해  기존  전체 사진기준 bbox를 좌표의 min,max값으로 bbox를 줄여 재학습을 진행함</p>
        <p id="1d39d9c4-5a6d-4f24-9758-8e6176c7f7b9" class="">model2 = test loss : 0.0001 Accuracy : 99</p>
        <p id="a087767c-4edb-43a3-8252-4f0190b0e8ea" class=""></p>
        <h2 id="deabca04-ea88-43dd-980c-a8794eac2424" class="">모델1 + 모델2를 결합하여 테스트를 진행한 결과:</h2>
        <p id="13ba20c1-f27a-44d9-a231-b0c3063d7c88" class="">boundary_size is 10, count of overrange : 0, Accuracy: 100.0%</p>
        <p id="89a70889-2162-4a98-8301-c3fa6d4e7fcf" class="">boundary_size is 15, count of overrange : 0, Accuracy: 100.0%</p>
        <p id="50f5dff1-449b-4b54-b5fb-ae7cbc238473" class="">boundary_size is 20, count of overrange : 0, Accuracy: 100.0%</p>
        <p id="3020f98b-073b-4a0d-9441-ccea8fa1302e" class="">boundary_size is 30, count of overrange : 0, Accuracy: 100.0%</p>
        <p id="4dcd9b4e-17b3-420c-8016-07a6ec83796b" class="">boundary_size is 40, count of overrange : 4, Accuracy: 98.67549668874172%</p>
        <p id="aebbd7c6-7065-42b1-986c-852b09efa321" class=""></p>
        <h2 id="cdbfcd1a-27bb-459e-95fd-85fb0e16bba3" class="">모델을 통해 생성된 keypoint를 이용한 왼손 정방향 조정 코드:</h2>
        <pre id="8e83df17-2a69-4fa7-acb1-f2ff752d0c48" class="code">
        <code>
def rotation(image, angleInDegrees):
    h, w = image.shape[:2]
    img_c = (w / 2, h / 2)
    rot = cv2.getRotationMatrix2D(img_c, angleInDegrees, 1)
    rad = math.radians(angleInDegrees)
    sin = math.sin(rad)
    cos = math.cos(rad)
    b_w = int((h * abs(sin)) + (w * abs(cos)))
    b_h = int((h * abs(cos)) + (w * abs(sin)))
    rot[0, 2] += ((b_w / 2) - img_c[0])
    rot[1, 2] += ((b_h / 2) - img_c[1])
    outImg = cv2.warpAffine(image, rot, (b_w, b_h), flags=cv2.INTER_LINEAR)
    return outImg
def position_checker(image_path,top,middle,thumb):
    img = cv2.imread(image_path)
    try:
        angle = math.atan2(top[0]-middle[0],middle[1]-top[1])
        angle = math.degrees(angle)
        print(angle)
        #시계방향 90도
        if 45&lt;= angle&lt;=135:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            image_height, image_width = img.shape[0], img.shape[1]
            top[0], top[1] = top[1],image_height -  top[0]
            middle[0], middle[1] = middle[1], image_height - middle[0]
            thumb[0], thumb[1] = thumb[1], image_height - thumb[0]
        #반시계방향 90도
        elif -135&lt;= angle&lt;=-45:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            image_height, image_width = img.shape[0], img.shape[1]
            top[0], top[1] = image_width - top[1], top[0]
            middle[0], middle[1] = image_width - middle[1], middle[0]
            thumb[0], thumb[1] = image_width - thumb[1], thumb[0]
        #180도
        elif 135&lt;= angle&lt;=225 or -225&lt;=angle&lt;=-135:
            img = cv2.rotate(img, cv2.ROTATE_180)
            image_height, image_width = img.shape[0], img.shape[1]
            top[0],top[1] = image_width - top[0],image_height-top[1]
            middle[0],middle[1] = image_width - middle[0],image_height - middle[1]
            thumb[0],thumb[1] = image_width - thumb[0],image_height - thumb[1]
        #좌우 대칭
        if middle[0] &gt; thumb[0]:
            img = cv2.flip(img, 1)
            image_height, image_width = img.shape[0], img.shape[1]
            top[0] = image_width - top[0]
            middle[0] = image_width - middle[0]
            thumb[0] = image_width - thumb[0]
        #양손 사진일 경우 왼손만 인식하기 위해 사진크기 조정
        image_height, image_width = img.shape[0], img.shape[1]
        if middle[0] &lt; image_width//2 and top[0]&lt; image_width//2 and thumb[0]&lt; image_width//2:
            flip_thumb_x = image_width - thumb[0]
            cutting_x_position = thumb[0]+flip_thumb_x/5
            img = img[0:image_height, 0: int(cutting_x_position)]
        #좌표에 점 찍기
        img = cv2.circle(img, (int(top[0]),int(top[1])), 6, (0, 0, 255), -1)
        img = cv2.circle(img, (int(middle[0]),int(middle[1])), 6, (0, 0, 255), -1)
        img = cv2.circle(img, (int(thumb[0]),int(thumb[1])), 6, (0, 0, 255), -1)
        angle = math.atan2(top[0] - middle[0], middle[1] - top[1])
        angle = math.degrees(angle)
        if -60&lt;=angle&lt;=60:
            img = rotation(img,angle)
            </code>
            </pre>
  <h2 id="24bda9a0-e73f-432f-bf06-69c0e4e1c7d3" class="">왼손 인식</h2>
  <div id="1aa746ca-3c7b-4012-9be4-7281c6e6470d" class="column-list">
    <div id="e246aa59-b32d-4067-96de-7b921a095e77" style="width:50%" class="column">
      <figure id="d9da19c5-fae3-474c-8565-70a6331eace2" class="image">
        <a href="image/many_hands.jpg">
          <img style="width:240px" src="image/many_hands.jpg" width="30%" height="30%"/>
        </a>
      </figure>
      <p id="396a1bb8-dccf-4e5d-b33d-fbd95c17e4cb" class="">원본사진</p>
    </div>
    <div id="ec1547b6-1e03-45ef-b965-5a1df81661dd" style="width:50%" class="column">
      <figure id="5bbfacb8-ae49-4152-bbdd-a2308e6a3df7" class="image">
        <a href="image/detect_many_hands.jpg">
          <img style="width:240px" src="image/detect_many_hands.jpg" width="30%" height="30%"/>
        </a>
      </figure>
      <p id="32a65acf-617a-4975-acda-788345b3fe7a" class="">조정된 사진</p>
    </div>
  </div>
  <h2 id="77a3996d-99d1-48a0-a6f7-c1fe737e581d" class="">90도의 사진을 정방향으로 조정</h2>
  <div id="8cccc1e7-60b9-4dbe-8b88-df27a29e864d" class="column-list">
    <div id="de587507-e90e-4f78-b067-cc694adba5b6" style="width:50%" class="column">
      <figure id="e5d76168-f49e-4c00-a163-32033c6dc2a9" class="image">
        <a href="image/90rotate.jpg">
          <img style="width:2044px" src="image/90rotate.jpg" width="30%" height="30%"/>
        </a>
      </figure>
      <p id="84ba38a1-4947-43d3-b59e-ecfd6ee42da3" class="">원본사진</p>
    </div>
    <div id="34bd5bbd-579b-45e6-8a2c-09c6b04854c3" style="width:50%" class="column">
      <figure id="2859a162-1801-43b3-b0cf-57e5134d8d95" class="image">
        <a href="image/modified_90rotate.jpg">
          <img style="width:192px" src="image/modified_90rotate.jpg" width="30%" height="30%"/>
        </a>
      </figure>
      <p id="4e219647-826d-4204-82c2-c331904253e9" class="">조정된 사진</p>
    </div>
  </div>
  <h2 id="34ead625-52ff-4de0-a2f1-ebfb28da93cd" class="">대칭된 사진을 정방향으로 조정</h2>
  <div id="586b4586-7247-47cc-aeb0-4e473a0d4aa4" class="column-list">
    <div id="c00f0a0e-31be-41b5-aeb9-c6b98353db05" style="width:50%" class="column">
      <figure id="57dac6b1-afbc-4b4b-b071-2131ed0f6dce" class="image">
        <a href="image/flip.jpg">
          <img style="width:240px" src="image/flip.jpg" width="30%" height="30%"/>
        </a>
      </figure>
      <p id="1062df37-62f5-4c03-b982-cd63e046ed26" class="">원본사진</p>
    </div>
    <div id="e1a07b5a-9667-4e34-a524-e9e208126283" style="width:50%" class="column">
      <figure id="2967e96b-8a0c-4647-bb38-c0aad03bd2a3" class="image">
        <a href="image/modified_flip.jpg">
          <img style="width:240px" src="image/modified_flip.jpg" width="30%" height="30%"/>
        </a>
      </figure>
      <p id="d8962a5a-2c12-4305-ab82-d03b5ae70628" class="">조정된 사진</p>
    </div>
  </div>
  <h2 id="91461e65-c179-45ca-8f56-fce493337518" class="">양손에서 왼손만 잘라서 사진 생성</h2>
  <div id="5eb0cfc2-0a3e-4612-b844-4b44c5e4d51a" class="column-list">
    <div id="1d639c80-374b-4ad0-959c-b69e3340d904" style="width:50%" class="column">
      <figure id="44e46c47-5c1b-41d6-a4da-7e22cc1160ad" class="image">
        <a href="image/hands.jpg">
          <img style="width:2033px" src="image/hands.jpg" width="30%" height="30%"/>
        </a>
      </figure>
      <p id="73ce0414-f7c8-456a-85ee-424a1692d4cb" class="">원본사진</p>
    </div>
    <div id="313f4fbf-c62d-471a-bbd8-a392a87df129" style="width:50%" class="column">
      <figure id="22e8c44b-194b-4935-a074-13e541a19627" class="image">
        <a href="image/crap_hands.jpg">
          <img style="width:192px" src="image/crap_hands.jpg" width="30%" height="30%"/>
        </a>
      </figure>
      <p id="2382111c-d495-436d-991b-c5eb962a5d89" class="">조정된 사진</p>
    </div>
  </div>
  <p id="64045d98-9dd7-45b8-9ba3-9a75be9fc4aa" class=""></p>
  </div>
  </article>
  </body>
</html>
