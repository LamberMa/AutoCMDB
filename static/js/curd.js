(function (jq) {

    var GLOBAL_DICT = {};
    var CREATE_SEARCH_CONDITION = true;

    // 为字符串创建可以像Python那样的字符串的格式化方法
    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
    };

    function getSearchCondition() {
        var conditon = {};
        $('.search-list').find('input[type=text],select').each(function () {
            // $(this)，这个要不就是input框，要你就是select，获取所有搜索条件
            var name = $(this).attr('name');
            var value = $(this).val();
            console.log(name, value);
            if (conditon[name]) {
                conditon[name].push(value)
            } else {
                conditon[name] = [value]
            }
        });
        return conditon;
    }

    function initial(url) {
        // 执行一个函数，获取当前搜索条件，没有条件的时候拿到的是一个空对象
        var searchCondition = getSearchCondition();
        console.log(searchCondition);
        $.ajax({
            url: url,
            type: 'GET',
            data: {'condition': JSON.stringify(searchCondition)},
            dataType: 'JSON',
            success: function (arg) {
                /*
                server_list: 相关资产信息
                table_config: 自定义的表配置
                global_dict: 相关的状态信息
                * */
                $.each(arg.global_dict, function (k, v) {
                    GLOBAL_DICT[k] = v;
                });
                initTableHeader(arg.table_config);
                initTableBody(arg.server_list, arg.table_config);
                initSearch(arg.search_config);
            }
        })
    }

    function initSearch(search_config) {
        // 有可能有的人没有设置，没有设置的时候其实就是一个undefined
        if (search_config && CREATE_SEARCH_CONDITION) {
            CREATE_SEARCH_CONDITION = false;
            // 找到搜索框的ul的位置，在里面动态添加li
            $.each(search_config, function (k, v) {
                var li = document.createElement('li');
                $(li).attr('search_type', v.search_type);
                $(li).attr('name', v.name);
                if (v.search_type === 'select') {
                    $(li).attr('global_name', v.global_name);
                }
                var a = document.createElement('a');
                a.innerHTML = v.text;
                li.append(a);
                $('.searchArea').find('ul').append(li)
            });

            // 初始化搜索默认条件，直接设置defaultcondition的值就可以了。
            var defaultcondition = search_config[0];
            $('.search-item .searchDefault').text(defaultcondition.text);
            // 替换搜索框的标签，如果search_type为select就换成下拉框
            if (defaultcondition.search_type === 'select') {
                var $sel = $('<select>');
                $sel.addClass('form-control');
                $sel.attr('name', defaultcondition.name);
                $.each(GLOBAL_DICT[defaultcondition.global_name], function (k, v) {
                    var option = document.createElement('option');
                    $(option).text(v[1]);
                    $(option).val(v[0]);
                    $sel.append(option);
                });

                $('.input-group').append($sel);
            } else {
                var $inp = $('<input>');
                $inp.addClass('form-control');
                $inp.attr('name', search_config[0].name);
                $inp.prop('type', 'text');
                $('.input-group').append($inp);
            }
        }
    }

    function initTableHeader(table_config) {
        // 为了保证刷新，所以这里每一次重新请求的时候先清空重新填写数据
        $('#tbhead').empty();
        var $tr = $('<tr>');
        $.each(table_config, function (k, v) {
            if (v.display) {
                var tag = document.createElement('th');
                tag.innerHTML = v.title;
                $tr.append(tag);
            }
        });
        $('#tbhead').append($tr);
    }

    function initTableBody(server_list, table_config) {
        // 同tbhead
        $('#tbbody').empty();
        $.each(server_list, function (k, row) {
            var tr = document.createElement('tr');
            tr.setAttribute('nid', row.id);
            $.each(table_config, function (tbconfig_key, tbconfig_value) {
                if (tbconfig_value.display) {
                    var td = document.createElement('td');

                    /* 在td标签中添加内容 */
                    var newKwargs = {};
                    $.each(tbconfig_value.text.kwargs, function (tpkey, tpvalue) {
                        var item = tpvalue;
                        if (tpvalue.substring(0, 2) === '@@') {
                            var choices = GLOBAL_DICT[tpvalue.substring(2, tpvalue.length)];
                            var nid = row[tbconfig_value.q];
                            $.each(choices, function (gk, gv) {
                                if (gv[0] === nid) {
                                    item = gv[1];
                                }
                            })
                        } else if (tpvalue[0] === "@") {
                            item = row[tpvalue.substring(1, tpvalue.length)];
                        }
                        newKwargs[tpkey] = item;
                    });
                    var newText = tbconfig_value.text.tpl.format(newKwargs);
                    td.innerHTML = newText;

                    /* 为td属性设置属性 */
                    $.each(tbconfig_value.attrs, function (attrkey, attrvalue) {
                        if (attrvalue[0] === '@') {
                            attrvalue = row[attrvalue.substring(1, attrvalue.length)];
                        }
                        td.setAttribute(attrkey, attrvalue);
                    });

                    $(tr).append(td)
                }
            });
            $('#tbbody').append(tr);
        });

    }

    function trIntoEdit($tr) {
        $tr.children('td[edit-enable="true"]').each(function () {
            // $(this)就是循环的每一个td对象
            // 如果传过来的没有设置的话就是undefined，设置的就是设置的值。
            var editType = $(this).attr('edit-type');
            if (editType === 'select') {
                // 生成下拉框
                var $tag = $('<select>');
                var device_type_choices = GLOBAL_DICT[$(this).attr('global-key')];
                var origin = $(this).attr('origin');
                $.each(device_type_choices, function (key, value) {
                    // value才是真正的数据，v.0是id，v1是名称
                    var $option = $('<option>');
                    $option.text(value[1]);
                    $option.val(value[0]);
                    // 设置默认值
                    if (value[0] == origin) {
                        $option.prop('selected', true);
                    }
                    $tag.append($option);
                });
                // 把内容放到td下
                $(this).html($tag);

            } else {
                // 获取原来的td标签的内容
                var text = $(this).text();
                // 创建一个input标签并设置里面的内容。
                var $tag_input = $('<input>');
                $tag_input.val(text);
                $(this).html($tag_input);
            }

        })
    }

    function trOutEdit($tr) {
        $tr.children('td[edit-enable="true"]').each(function () {
            var editType = $(this).attr('edit-type');
            if (editType === 'select') {
                // 首先要拿到默认选中的值。
                /**
                 * DOM对象转换为jq对象，只要用$()把dom对象包装起来就可以得到了。
                 * jq对象转换为dom对象的时候在后面加一个"[0]"就可以了。
                 * 这里将select的jq对象转换为dom对象调用selectedOptions方法。
                 * */
                var option = $(this).find('select')[0].selectedOptions;
                $(this).attr('new-origin', $(option).val());
                $(this).html($(option).text());
            } else {
                var input_val = $(this).find('input').val();
                $(this).html(input_val);
            }

        })
    }

    jq.extend({
        curd: function (url) {
            initial(url);
            // 这个匿名函数的各种作用域包含上述的函数在外部都是不可调用的，唯一的入口就是我们
            // 自己定义的这个扩展的jq的curd可以使用到。
            // 这种绑定方式的要求是先得有数据，没有数据的话是绑定不上的。后加的数据绑定不上
            // 因此要使用on的方式进行绑定
            // $('#tbbody').find(':checkbox').click(function () {
            //    $(this)
            //});

            // 对所有的checkbox绑定时间
            $('#tbbody').on('click', ':checkbox', function () {
                //
                /**
                 * $(this)表示当前的checkbox标签
                 * 1.点击首先检测是否进入编辑模式，如果是，就退出，不是就进入
                 */
                var $tr = $(this).parent().parent();
                // 否则什么都不做，因为本来就是直接点不进入编辑模式的。
                if ($('#editmodelornot').hasClass('btn-warning')) {
                    if ($(this).prop('checked')) {
                        // 进入编辑模式
                        trIntoEdit($tr);
                    } else {
                        // 退出编辑模式
                        trOutEdit($tr)
                    }
                }
            });

            // 对所有的按钮绑定时间
            $('#checkAll').click(function () {
                var $tbbody = $('#tbbody');
                // $tbbody.find(':checkbox').prop('checked', true);
                // // 选中每一个进入编辑模式
                // $tbbody.find('tr').each(function () {
                //     trIntoEdit($(this));
                // });
                /**
                 * 首先全选的时候应该让这一行进入编辑模式，但是我们发现通过事件触发和我们手动点击不一样
                 * 手动点击会触发编辑模式，但是事件触发checked并不会进入编辑模式，因此我们需要手动调用一下
                 * 但是这还有一个问题就是，假如说全选的时候已经有一个内容被选中了，假如说这个内容是一个内容框
                 * 在选中以后会被改为input框，在trIntoEdit中，我们会先去获取此时td的值，然后将这个td的内容
                 * 改为一个input框再把这个值动态的填进去设置为input的value值，此时在input框中value有值，但是text为空
                 * 如果此时再执行全选调用一个trIntoEdit事件的时候，这个时候拿到的数据就是空的了。因为text的是空的
                 * 我们看到的input框有值，那是因为input框的value属性是有值的！！！！！
                 * 此时会看到数据变为空值，因此我们在做的时候需要自行判断一下，因此上面的方法是不可行的
                 * */
                if ($('#editmodelornot').hasClass('btn-warning')) {
                    $tbbody.find(':checkbox').each(function () {
                        if (!$(this).prop('checked')) {
                            $(this).prop('checked', true);
                            var $tr = $(this).parent().parent();
                            trIntoEdit($tr)
                        }
                    })
                } else {
                    $tbbody.find(':checkbox').prop('checked', true);
                }


            });

            $('#checkReverse').click(function () {
                if ($('#editmodelornot').hasClass('btn-warning')) {
                    $('#tbbody').find(':checkbox').each(function () {
                        var $tr = $(this).parent().parent();
                        if ($(this).prop('checked')) {
                            $(this).prop('checked', false);
                            trOutEdit($tr);
                        } else {
                            $(this).prop('checked', true);
                            trIntoEdit($tr);
                        }
                    })
                } else {
                    $('#tbbody').find(':checkbox').each(function () {
                        var $tr = $(this).parent().parent();
                        if ($(this).prop('checked')) {
                            $(this).prop('checked', false);
                        } else {
                            $(this).prop('checked', true);
                        }
                    })
                }

            });

            $('#checkCancel').click(function () {
                if ($('#editmodelornot').hasClass('btn-warning')) {
                    $('#tbbody').find(':checkbox').each(function () {
                        if ($(this).prop('checked')) {
                            $(this).prop('checked', false);
                            var $tr = $(this).parent().parent();
                            trOutEdit($tr)
                        }
                    })
                } else {
                    $('#tbbody').find(':checkbox').prop('checked', false);
                }

            });

            $('#editmodelornot').click(function () {
                if ($(this).hasClass('btn-warning')) {
                    // 我们定义的就是进入编辑模式的时候会变成btn-waring的这个样式，也就是可以通过
                    // 判断是否有这个样式来判断是否已经进入了编辑模式
                    // 如果有这个css class的话那么应该退出这个编辑模式
                    $(this).removeClass('btn-warning');
                    $(this).text('进入编辑模式');
                    $('#tbbody').find(':checkbox').each(function () {
                        var $tr = $(this).parent().parent();
                        if ($(this).prop('checked')) {
                            trOutEdit($tr);
                        }
                    })
                } else {
                    $(this).addClass('btn-warning');
                    $(this).text('退出编辑模式');
                    /**
                     * 还有一个问题就是我在未进入编辑模式的时候选中一些数据，然后再点进入编辑模式发现并不会变化
                     * 因此我们在进出编辑模式的时候不只是改改字换换样式啥的，也要做基础的判断是否选中。
                     * */
                    $('#tbbody').find(':checkbox').each(function () {
                        var $tr = $(this).parent().parent();
                        if ($(this).prop('checked')) {
                            trIntoEdit($tr);
                        }
                    })
                }
            });

            $('#multiDel').click(function () {
                var idList = [];
                console.log(url);
                $('#tbbody').find(':checked').each(function () {
                    idList.push($(this).val());
                });
                $.ajax({
                    url: url,
                    // form表单只能提交get或者post请求，但是对于ajax delete也是ok的。
                    type: 'delete',
                    data: JSON.stringify(idList),
                    success: function (arg) {
                        console.log(arg)
                    }
                })
            });

            $('#refresh').click(function () {
                // 刷新一遍重新拿数据
                initial(url);
            });

            $('#save').click(function () {
                // 设计为首先推出编辑模式以后才能保存
                if ($('#editmodelornot').hasClass('btn-warning')) {
                    // 在编辑模式下应该退出
                    $('#tbbody').find(':checkbox').each(function () {
                        if ($(this).prop("checked")) {
                            var $tr = $(this).parent().parent();
                            trOutEdit($tr);
                        }
                    })
                }
                // 定一个修改资产的列表总表，下面去循环每一个发生变化的项然后append进来
                var all_list = [];
                // 退出以后获取用户修改过的数据，然后通过ajax提交到后台
                $('#tbbody').children().each(function () {

                    // $(this)这里指的就是tr
                    var $tr = $(this);
                    var nid = $tr.attr('nid');
                    var row_dict = {};
                    var flag = false;
                    $tr.children().each(function () {
                        // 要判断是否可编辑，同时还要判断下拉框的情况下
                        if ($(this).attr('edit-enable') === 'true') {
                            if ($(this).attr('edit-type') == 'select') {
                                var newData = $(this).attr('new-origin');
                                var oldData = $(this).attr('origin');
                                if (newData) {
                                    if (newData != oldData) {
                                        var name = $(this).attr('name');
                                        row_dict[name] = newData;
                                        // 如果写过数据就置位为true
                                        flag = true;
                                    }
                                }
                            } else {
                                var newData = $(this).text();
                                var oldData = $(this).attr('origin');
                                if (newData != oldData) {
                                    var name = $(this).attr('name');
                                    row_dict[name] = newData;
                                    // 如果写过数据就置位为true
                                    flag = true;
                                }
                            }

                        }
                    });
                    // 如果没有编辑的话dict可能为空，因此要做一下判断
                    if (flag) {
                        row_dict['id'] = nid;
                    }
                    all_list.push(row_dict);
                });
                /**
                 * RestfulApi
                 * 添加：post；获取用get；删除：delete；修改:put
                 * */
                $.ajax({
                    url: url,
                    method: 'PUT',
                    data: JSON.stringify(all_list),
                    success: function (arg) {
                        console.log(arg);
                    }
                })
            });

            // 搜索框选择不同的类型的时候对应的类型也要变，一开始的时候是没有li的
            $('.search-list').on('click', 'li', function () {
                // 点击li执行函数
                var li_text = $(this).text();
                var search_type = $(this).attr('search_type');
                var name = $(this).attr('name');
                var global_name = $(this).attr('global_name');

                // 替换显示的文本
                $(this).parent().prev().children('.searchDefault').text(li_text);

                // 替换搜索框的标签，如果search_type为select就换成下拉框
                if (search_type === 'select') {
                    var $sel = $('<select>');
                    $sel.addClass('form-control');
                    $sel.attr('name', name);
                    $.each(GLOBAL_DICT[global_name], function (k, v) {
                        option = document.createElement('option');
                        $(option).text(v[1]);
                        $(option).val(v[0]);
                        $sel.append(option);
                    });

                    $(this).parent().parent().next().remove();
                    $(this).parent().parent().after($sel);
                } else {
                    var $inp = $('<input>');
                    $inp.addClass('form-control');
                    $inp.attr('name', name);
                    $inp.prop('type', 'text');
                    $(this).parent().parent().next().remove();
                    $(this).parent().parent().after($inp);
                }

            });

            $('.search-list').on('click', '.add-search-condition', function () {
                if ($(this).children('span').hasClass('glyphicon-plus')) {
                    /**
                     * 如果我当前点击a标签的符号是一个加号的话那么就执行加的操作
                     * 1、克隆一个search-item
                     * 2、然后把这个item下的a标签中的span的class改为减号"glyphicon-plus"
                     * */
                    var newSearchItem = $(this).parent().parent().clone();
                    $(newSearchItem).find('.add-search-condition').find('span').removeClass('glyphicon-plus').addClass('glyphicon-minus');
                    $('.search-list').append(newSearchItem);
                } else {
                    /**
                     * 如果我点击的当前a标签的符号是一个减号的话，那么应该执行一个删除的操作，把当前的点击的这个item给删除掉
                     * */
                    $(this).parent().parent().remove();
                }

            })

            $('#doSearch').click(function () {
                /**
                 * 获取input框，或者select框，获取name和value
                 * 通过ajax提交到后台。
                 * */
                initial(url);
            })
        }
    })


})(jQuery);

