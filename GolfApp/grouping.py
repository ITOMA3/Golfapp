import random  # randomモジュールをインポート

def group_participants(participants):
    print("グループ分け開始前の参加者リスト:", [p.name for p in participants])
    
    # 参加者リストをシャッフル
    random.shuffle(participants)
    
    leaders = [p for p in participants if p.is_etiquette_leader]
    women = [p for p in participants if p.gender == 'F' and not p.is_etiquette_leader]
    others = [p for p in participants if not p.is_etiquette_leader and p.gender != 'F']
    
    # 参加者の総数に基づいて必要なグループ数を計算
    total_participants = len(participants)
    num_groups = (total_participants + 3) // 4  # 4名で割り切れない場合は追加のグループを作成
    
    # グループの枠を作成
    groups = [[] for _ in range(num_groups)]
    
    # エチケットリーダーを各グループに1人ずつ割り当て
    for leader in leaders:
        for group in groups:
            if len(group) < 4:
                group.append(leader)
                break
    
    # 女性を各グループに1人ずつ割り当て
    for woman in women:
        for group in groups:
            if len(group) < 4 and not any(p.gender == 'F' for p in group):
                group.append(woman)
                break
    
    # 残りの参加者を割り当て
    for other in others:
        for group in groups:
            if len(group) < 4:
                group.append(other)
                break
    
    # 3名以下のグループがあれば調整
    # 最後のグループが3名未満の場合、他のグループから人を移動
    while len(groups[-1]) < 3:
        for group in groups[:-1]:
            if len(group) > 3:
                groups[-1].append(group.pop())
                break
    
    print("グループ分け結果:", [[p.name for p in group] for group in groups])
    return groups