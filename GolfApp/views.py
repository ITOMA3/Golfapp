from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .grouping import group_participants
from .models import Participant
from django.contrib import messages  # メッセージフレームワークをインポート
from django.shortcuts import render
from django.views.generic.edit import UpdateView


class ParticipantCreateView(CreateView):
    model = Participant
    fields = ['name', 'average_score', 'gender', 'is_etiquette_leader']
    template_name = 'participant_form.html'
    success_url = reverse_lazy('index')  # 登録後にトップページにリダイレクト

def index(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('participants[]')
        print("選択された参加者ID:", selected_ids)
        selected_participants = Participant.objects.filter(id__in=selected_ids)
        if len(selected_participants) < 3:
            needed_participants = 3 - len(selected_participants)
            messages.error(request, f'参加者が足りません。あと{needed_participants}名の参加者が必要です。')
            return redirect('index')

        # 選択された参加者のみをグループ分けする
        groups = group_participants(list(selected_participants))
        print(selected_participants)
        if any(len(group) < 3 for group in groups):
            messages.error(request, 'グループ分けに失敗しました。各グループは3名以上でなければなりません。')
            return redirect('index')
        
        # グループ分けの結果をセッションに保存
        request.session['groups'] = [[participant.id for participant in group] for group in groups]
        
        return redirect('group_results')
    else:
        participants = Participant.objects.all()
        return render(request, 'index.html', {'participants': participants})
def group_results(request):
    # セッションからグループIDのリストを取得
    group_ids = request.session.get('groups', [])
    
    # 取得したグループIDのリストをコンソールに出力
    print("取得したグループIDのリスト:", group_ids)
    
    # グループIDから参加者オブジェクトのリストを再構築
    groups = [Participant.objects.filter(id__in=group) for group in group_ids]
    
    # 再構築したグループのリストをコンソールに出力
    print("再構築したグループのリスト:")
    for i, group in enumerate(groups, start=1):
        print(f"グループ {i}: {[participant.name for participant in group]}")
    
    return render(request, 'group_results.html', {'groups': groups})

def delete_participants(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('delete_participants[]')
        Participant.objects.filter(id__in=selected_ids).delete()
        messages.success(request, '選択された参加者を削除しました。')
    return redirect('index')

def show_delete_participants_form(request):
    participants = Participant.objects.all()
    return render(request, 'delete_participants.html', {'participants': participants})

class ParticipantUpdateView(UpdateView):
    model = Participant
    fields = ['name', 'average_score', 'gender', 'is_etiquette_leader']
    template_name = 'participant_edit_form.html'
    success_url = reverse_lazy('index')  # 編集後にトップページにリダイレクト