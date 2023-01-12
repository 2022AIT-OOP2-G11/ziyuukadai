// <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script>
{
  /* <script language="javascript" type="text/javascript" src="/static/index.js"> */
}
// </script>
// ↑HTMLにこれ入れる

$.getJSON("/static/sample.json", (data) => {
  console.log(data);
});
