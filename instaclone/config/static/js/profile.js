// 마이페이지 - 내가쓴글, 북마크 클릭 이벤트

const tapContainer = document.querySelector('.about');
const flex_Container = document.querySelectorAll('.contents_container');
const taps = document.querySelectorAll('.about > span');


function openCity(e) {

    let element = e.target;


    for(let i = 0; i < flex_Container.length; i++) {
        flex_Container[i].classList.remove('active');
        taps[i].classList.remove('on');

        console.log('flex_Container[i]: ', flex_Container[i]);
        console.log('taps[i]: ', taps[i]);

    }


    if(element.matches('[class="nick_name"]')) {
        console.log('nick_name');

        flex_Container[0].classList.add('active');
        taps[0].classList.add('on');

    } else if(element.matches('[class="book_mark"]')) {
        console.log('book_mark');

        flex_Container[1].classList.add('active');
        taps[1].classList.add('on');
    }


}


tapContainer.addEventListener('click', openCity);