
fetch("sample.json")
.then(response => {
    return response.json();
})
.then(jsondata => console.log(jsondata));
// window.onload = function(){
//     // ページ読み込み時に実行したい処理
// }