import random

from fastapi import APIRouter
from fastapi import Form
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory='templates')
theme_and_location = {
    'Школа': [
        'Клас фізики', 'Клас хімії', 'Клас інформатики', 'Клас історії', 'Клас географії', 'Бібліотека',
        'Столова', 'Кабінет директора', 'Кабінет вчителя', 'Перевдягальня', 'Душова', 'Туалет', 'Коридор',
        'Кабінет психолога', 'Кабінет лікаря', 'Кабінет вихователя', 'Кабінет педагога-організатора', 'Актовий зал',
    ],
    'Ресторан': [
        'Кухня', 'Зал', 'Бар', 'Туалет', 'Коридор', 'Кабінет директора', 'Кабінет кухаря', 'Кабінет офіціанта',
        'Кабінет бармена', 'Кабінет вахтера', 'Кабінет касира', 'Кабінет повара', 'Кабінет вантажника',
        'Кабінет охоронця', 'Кабінет менеджера', 'Кабінет бухгалтера', 'Кабінет керівника'
    ],
    'Банк': [
        'Каса', 'Кабінет клієнта', 'Кабінет менеджера', 'Кабінет касира', 'Кабінет охоронця', 'Кабінет бухгалтера',
        'Кабінет директора', 'Кабінет кредитного інспектора', 'Кабінет кредитного менеджера'
    ],
    'Лікарня': [
        'Приймальне', 'Палата', 'Операційний зал', 'Кабінет лікаря', 'Кабінет медсестри', 'Кабінет адміністратора',
        'Кабінет лаборанта', 'Кабінет рентгенолога', 'Кабінет терапевта', 'Кабінет хірурга', 'Кабінет анестезіолога',
        'Кабінет психіатра', 'Кабінет психолога', 'Кабінет фармацевта', 'Кабінет медичного брата'
    ],
    'Поліція': [
        'Приймальне', 'Кабінет допиту', 'Кабінет слідчого', 'Кабінет оперуповноваженого', 'Кабінет криміналіста',
        'Кабінет кримінального аналітика', 'Кабінет оперативника', 'Кабінет патрульного',
        'Кабінет кримінального кодексу',
    ],
    'Подорож': [
        'Поїзд', 'Автобус', 'Таксі', 'Літак', 'Корабель', 'Велосипед', 'Мотоцикл', 'Автомобіль', 'Скутер', 'Санки',
        'Снігокат', 'Коні', 'Верблюд', 'Корова', 'Кінь', 'Коза', 'Свиня', 'Собака', 'Кіт', 'Хом'
    ],
}

game_state = {
    'selected_location': None,
    'spy_index': None,
    'is_game_active': False,
    'players': [],
    'theme': None,
    'location': None,
}


@router.get('/')
async def home(request: Request):
    return templates.TemplateResponse('welcome.html', {'request': request})


@router.get('/setup-game/')
async def setup_game_form(request: Request):
    return templates.TemplateResponse('setup_game.html', {'request': request})


@router.post('/setup-game/')
async def setup_game(
        request: Request,
        player_count: int = Form(...),
        player_1: str = Form(...),
        player_2: str = Form(...),
        player_3: str = Form(...),
        player_4: str = Form(None),
        player_5: str = Form(None),
        player_6: str = Form(None),
        player_7: str = Form(None),
        player_8: str = Form(None),
        player_9: str = Form(None),
        player_10: str = Form(None)
):
    players = [player_1, player_2, player_3]
    optional_players = [player_4, player_5, player_6, player_7, player_8, player_9, player_10]

    for player in optional_players:
        if player:
            players.append(player)

    if len(players) != player_count:
        return templates.TemplateResponse(
            'setup_game.html', {
                'request': request,
                'message': 'Помилка у введенні гравців. Спробуйте ще раз.'
            }
        )

    game_state['players'] = players
    game_state['spy_index'] = random.randint(0, len(players) - 1)
    game_state['is_game_active'] = True
    theme = random.choice(list(theme_and_location.keys()))
    game_state['selected_theme'] = theme
    game_state['selected_location'] = random.choice(theme_and_location[theme])

    return RedirectResponse('/show-next-player/', status_code=303)


@router.get('/show-next-player/')
async def show_next_player(request: Request):
    if not game_state['is_game_active']:
        return RedirectResponse('/', status_code=303)

    if 'current_player_index' not in game_state:
        game_state['current_player_index'] = 0

    current_index = game_state['current_player_index']
    player = game_state['players'][current_index]

    if current_index == game_state['spy_index']:
        player_info = {
            'player': player,
            'info': f'Тема: {game_state['selected_theme']}. \n\nВИ ШПИГУН! \n\nВаша задача — дізнатися місце.',
        }
    else:
        player_info = {
            'player': player,
            'info': f'Тема: {game_state['selected_theme']}. \nМісце: {game_state['selected_location']}',
        }

    game_state['current_player_index'] = (current_index + 1) % len(game_state['players'])

    return templates.TemplateResponse('show_player.html', {
        'request': request,
        'player_info': player_info
    })


@router.get('/character-info/')
async def character_info(request: Request):
    start_index = random.randint(0, len(game_state['players']) - 1)

    return templates.TemplateResponse('character_info.html', {
        'request': request,
        'player': game_state['players'][start_index],
    })


@router.get('/question-stage/')
async def question_stage(request: Request):
    if not game_state['is_game_active']:
        return RedirectResponse('/', status_code=303)

    if 'question_order' not in game_state:
        players = game_state['players'].copy()
        random.shuffle(players)
        question_order = []

        for i in range(len(players)):
            current_player = players[i]
            next_player = players[(i + 1) % len(players)]
            question_order.append((current_player, next_player))

        game_state['question_order'] = question_order
        game_state['current_question_index'] = 0

    current_index = game_state['current_question_index']
    current_question = game_state['question_order'][current_index]

    return templates.TemplateResponse('question_stage.html', {
        'request': request,
        'current_question': current_question,
        'remaining_questions': len(game_state['question_order']) - current_index - 1
    })


@router.post('/next-question/')
async def next_question(request: Request):
    if 'current_question_index' not in game_state or 'question_order' not in game_state:
        return RedirectResponse('/question-stage/', status_code=303)

    game_state['current_question_index'] += 1

    if game_state['current_question_index'] >= len(game_state['question_order']):
        return RedirectResponse('/discussion-stage/', status_code=303)

    return RedirectResponse('/question-stage/', status_code=303)


@router.get('/discussion-stage/')
async def discussion_stage(request: Request):
    if not game_state['is_game_active']:
        return RedirectResponse('/', status_code=303)

    return templates.TemplateResponse('discussion_stage.html', {
        'request': request
    })


@router.post('/declare-location/')
async def declare_location(request: Request, player: str = Form(...), guessed_location: str = Form(...)):
    if guessed_location == game_state['selected_location']:
        return templates.TemplateResponse('victory.html', {
            'request': request,
            'message': f'Гравець {player} (шпигун) правильно назвав місце! Шпигун переміг!'
        })
    else:
        return templates.TemplateResponse('discussion_stage.html', {
            'request': request,
            'message': f'Гравець {player} неправильно назвав місце. Гра продовжується.'
        })


@router.get('/restart-question-round/')
async def restart_question_round(request: Request):
    if 'question_order' in game_state:
        game_state['current_question_index'] = 0  # Перезапуск запитань
    return RedirectResponse('/question-stage/', status_code=303)
