$(function () {
       initial();
});


// 为字符串创建可以像Python那样的字符串的格式化方法
String.prototype.format = function (args) {
    return this.replace(/\{(\w+)\}/g, function (s,i) {
        return args[i];
    });
};

function initial() {
    $.ajax({
        url:'/backend/curd_json.html',
        type:'GET',
        dataType: 'JSON',
        success:function (arg) {
            /*
            * server_list就是所有的数据
            * table_config是所有的表头字段
            * */
            // 创建表头
            initTableHeader(arg.table_config);
            initTableBody(arg.server_list,arg.table_config);
        }
    })
}

function initTableHeader(table_config) {
    /*
    * 我现在要通过这个table_config动态的
    * 插入表格的表头，也就是th标签*/
    $.each(table_config,function (k,v) {
        var tag = document.createElement('th');
        tag.innerHTML = v.title;
        $('#tbhead').find('tr').append(tag);
    })
}

function initTableBody(server_list,table_config) {
    /*
    * server_list从后台发回来的数据是如下这样类似格式的：
    * [
    *   {"id": 1, "hostname": "\u9a6c\u6653\u96e8\u7684MBP"},
    *   {"id": 1, "hostname": "\u9a6c\u6653\u96e8\u7684MBP"},
    *   {"id": 1, "hostname": "\u9a6c\u6653\u96e8\u7684MBP"},
    * ]*/
    var tr = document.createElement('tr');
    $.each(server_list,function (k,row) {
        //row:{"id": 1, "hostname": "\u9a6c\u6653\u96e8\u7684MBP"},
        $.each(table_config,function (kk,rrow) {
            //这里把table_config引进来是为了解决字段乱序的问题
            //这样以后如果想要调整顺序的话就可以随便更换了，直接换后台配置文件就行了。
            // kk: 1 rrow: {'q':'id','title':'ID'}
            var td = document.createElement('td');
            // if(rrow['q']){
            //     td.innerHTML = row[rrow.q];
            // }else{
            //     console.log(rrow.text);
            //     td.innerHTML = rrow.text;
            // }

            // rrow['q']
            // rrow['text']
            // rrow.text.tpl = "asdasd{n1}asd"
            // rrow.text.kwargs = {'n1':'@id', 'n2':'as'}
            var newKwargs = {};
            $.each(rrow.text.kwargs, function (kkk,vvv) {
                var av = vvv;
                if(vvv[0] == "@"){
                    av = row[vvv.substring(1,vvv.length)];
                    console.log(av);
                }
                newKwargs[kkk] = av;
            });
            // var newText = rrow.text.tpl.format(rrow.text.kwargs);
            var newText = rrow.text.tpl.format(newKwargs);
            td.innerHTML = newText;
            $(tr).append(td)
        })
    });
    $('#tbbody').append(tr);
}