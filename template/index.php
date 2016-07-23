<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=devicd-width, initial-scale=1.0">
        <script src="/js/jquery-3.1.0.min.js"></script>
    </head>
    <style>
        td{padding:0 15px;}
    </style>
    <body>
        <table>
            <?php foreach($paperData as $key => $val): ?>
            <?php if($key % 4 == 0): ?>
            <tr style="width:100%;">
            <?php endif; ?>
                <td style=""><a href="<?php echo $pconlineUrl . $val['url']; ?>" target="_blank"><img src="<?php echo $val['image']; ?>"></a></td>
            <?php if(($key + 1) % 4 == 0): ?>
            </tr>
            <?php endif; ?>
            <?php endforeach; ?>
        </table>
    <script>
        var currentPage = <?php echo $page; ?>;
        var windowHeight = $(window).height();

        $(document).ready(function(){
            $('img').width($(window).width() / 4 - 35 + 'px');
            $('tr').height(windowHeight / 3 + 'px');

            $(document).keypress(function(event){
//alert(event.keyCode);return false;
                switch(event.keyCode){
                    case 37:
                        if(currentPage > 1){
                            window.location.href = "<?php echo $hostsUrl; ?>/?page=" + (currentPage - 1);
                        }
                        break;

                    case 39:
                        window.location.href = "<?php echo $hostsUrl; ?>/?page=" + (currentPage + 1);
                        break;

                    case 38:
                        var htmlScrollTop = $('html').scrollTop() >= windowHeight / 3 ? $('html').scrollTop() : windowHeight / 3;
                        $('html').animate({scrollTop: htmlScrollTop - windowHeight / 3});
                        break;

                    case 40:
                        $('html').animate({scrollTop: $('html').scrollTop() + windowHeight / 3});
                        break;

                    default:
                        return;
                }
            });
        });
    </script>
    </body>
</html>
