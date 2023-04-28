$('input[type="submit"]').click(function(){
    $.ajax({
        url: '/sendWeather',
        type: 'POST',
        data: $('input[type="text"]').val(),

        beforeSend: function() {
            $('.icon').html(`<i class="bi spin bi-arrow-clockwise"></i>`)
            $('.icon').addClass('spin')
            $('#temp').html(`<p>Ожидание...</p>`)
        },

        success: function(res) {
            $('.icon').removeClass('spin')
            switch (res['Погода']) {
                case 'Туман':
                    $('.icon').html(`<i class="bi weather-icon bi-cloud-fog"></i>`)
                    break;
                case 'Облака':
                    $('.icon').html(`<i class="bi weather-icon bi-clouds"></i>`)
                    break
                case "Прозрачный":
                    $('.icon').html(`<i class="bi weather-icon bi-cloud-slash"></i>`)
                    break
                case "Дождь":
                    $('.icon').html(`<i class="bi weather-icon bi-cloud-rain"></i>`)
                    break
                case "Снег":
                    $('.icon').html(`<i class="bi weather-icon bi-cloud-snow"></i>`)
                    break
                default:
                    $('.icon').html(`<i class="bi weather-icon bi-thermometer"></i>`)
                    break;
            }
            $('#temp').html(`
            <div class='infoWeather'>
                    <div class='flex'><i class="bi bi-thermometer-half temp_icon"></i> <p>${res['Температура']}C˚</p></div>
                    <div class='flex'><i class="bi bi-wind temp_icon_small"></i> <p>${res['Ветер']}м/с</p></div>
            </div>
            `)

            if ($('.item-history').length == 4){
                $('.item-history')[3].remove()
            }

            $('.history').prepend(`
            <div class="item-history">
                <h1 class='history-h1'>${$('input[type="text"]').val()}</h1>
                ${$('.icon').clone().html()}
                <p>Температура: ${res['Температура']}C˚</p>
                <p>Ветер: ${res['Ветер']}м/с</p>
            </div>
            `)
            
            $.ajax({
                url: '/setHistory',
                type: 'POST',
                data: {
                    'city': $('input[type="text"]').val(),
                    'weather': res['Погода'],
                    'temp': res['Температура'],
                    'wind': res['Ветер']
                }
            })
            
        }
    })
})

$('.history').on('click', '.history-h1', function() {
    $('input[type="text"]').val($(this).text())
    $('input[type="submit"]').click()
})

$(document).ready(function () {
    $.ajax({
        url: '/setToken',
        type: 'POST',
        data: {'token': localStorage.getItem('weatherToken') || 'None'},

        success: function (res) {
            if (res['status'] == 'ok'){
                localStorage.setItem('weatherToken', res['token'])
            }
        }
    })
})