// 创始人QQ
let create_user_qq = "";

// 添加页面数据
function load_data(json_str) {
    let data_json = JSON.parse(json_str);

    create_user_qq = data_json["创始人QQ"];
    console.log("创始人QQ:" + create_user_qq);

    document.getElementById("code").innerText = '报名编号：' + data_json["编号"];
    document.getElementById("title").innerText = data_json["标题"];
    document.getElementById("group_num").innerText = "团队人数：" + data_json["用户列表"].length + "/" + data_json["副本最大人数"];

    // 创建表格，传入团本信息
    function create_table(data_json) {
        const table_div = document.getElementById('table_div')
        const table = document.createElement('table');
        table.id = "table1"
        table_div.appendChild(table);

        const thead = document.createElement('thead');
        table.appendChild(thead);
        const tr = document.createElement('tr');
        thead.appendChild(tr);
        const th0 = document.createElement('th');
        th0.style.width = "50px";
        const th1 = document.createElement('th');
        const th2 = document.createElement('th');
        const th3 = document.createElement('th');
        const th4 = document.createElement('th');
        const th5 = document.createElement('th');
        th0.innerHTML = '队伍';
        th1.innerHTML = '一';
        th2.innerHTML = '二';
        th3.innerHTML = '三';
        th4.innerHTML = '四';
        th5.innerHTML = '五';
        tr.appendChild(th0);
        tr.appendChild(th1);
        tr.appendChild(th2);
        tr.appendChild(th3);
        tr.appendChild(th4);
        tr.appendChild(th5);

        const tbody = document.createElement('tbody');
        table.appendChild(tbody);

        // 门派二维数组 内 外 肉 奶 （注意：这里改了，index.js也需要改）
        let sect_arrs = [
            ["焚影", "花间游", "花间", "莫问", "毒经",
            "dj", "紫霞功", "气纯", "天罗诡道", "田螺",
            "无方", "冰心", "易筋经", "和尚", "太玄经",
            "衍天"],
            ["藏剑", "太虚剑意", "剑纯", "惊羽诀", "鲸鱼", 
            "傲雪战意", "天策", "北傲", "霸刀", "隐龙", 
            "凌雪", "笑尘", "丐帮", "凌海诀", "蓬莱", 
            "分山劲", "苍云", "孤锋诀", "刀宗"],
            ["铁骨", "铁王八", "铁牢律", "策T", "明尊琉璃体",
            "喵T", "洗髓", "和尚T"],
            ["相知", "奶歌", "灵素", "药奶", "补天",
            "奶毒", "离经易道", "奶花", "云裳心经", "奶秀"]
        ];
        // 职位数组 内 外 肉 奶
        let neigong_arr = [];
        let waigong_arr = [];
        let rou_arr = [];
        let nai_arr = [];
        
        let boss_num = 0;

        // 分类职位 顺便计数 老板
        for (let i = 0; i < data_json["用户列表"].length; i++) {
            if (sect_arrs[0].indexOf(data_json["用户列表"][i]["门派"]) !== -1) {
                neigong_arr.push(data_json["用户列表"][i]);
            } else if (sect_arrs[1].indexOf(data_json["用户列表"][i]["门派"]) !== -1) {
                waigong_arr.push(data_json["用户列表"][i]);
            } else if (sect_arrs[2].indexOf(data_json["用户列表"][i]["门派"]) !== -1) {
                rou_arr.push(data_json["用户列表"][i]);
            } else if (sect_arrs[3].indexOf(data_json["用户列表"][i]["门派"]) !== -1) {
                nai_arr.push(data_json["用户列表"][i]);
            }

            if (data_json["用户列表"][i]["ID"].indexOf("老板") != -1) {
                boss_num++;
            }
        }

        document.getElementById("boss").innerHTML = '<p id="p_boss">老板：' + boss_num + '</p>';

        // 计算各职位数量
        document.getElementById("job").innerHTML = '<p id="p_sect">门派统计：</p>' +  
            '<p id="p_waigong">外功：' + waigong_arr.length + '</p>&nbsp;&nbsp;' +
            '<p id="p_neigong">内功：' + neigong_arr.length + '</p>&nbsp;&nbsp;' +
            '<p id="p_rou">T：' + rou_arr.length + '</p>&nbsp;&nbsp;' +
            '<p id="p_nai">奶妈：' + nai_arr.length + '</p>';

        // 遍历行
        for (let i = 0; i < 5; i++) {
            const tr = document.createElement('tr');
            tbody.appendChild(tr);

            // 遍历列
            for (let j = 0; j < 6; j++) {
                const td = document.createElement('td');
                td.id = "td_" + (i * 6 + j); 

                // 首列特殊处理
                if (j == 0) {
                    const td_content = ["一", "二", "三", "四", "五"];
                    td.innerHTML = td_content[i];
                    tr.appendChild(td);
                    continue;
                }

                td.innerHTML = "";
                tr.appendChild(td);
            }
        }

        // 各职业对应的td下标，含有通用的下标
        let waigong_index_arr = [1, 7, 13, 19, 25, 2];
        let neigong_index_arr = [3, 9, 15, 21, 27, 4];
        let waigong_naigong_index_arr = [8, 14, 20, 26, 10, 16];
        let rou_nai_index_arr = [5, 11, 17, 23, 29];
        let common_index_arr = [22, 28];

        for(let i = 0; i < waigong_arr.length; i++) {
            let firstValue = -1;
            if (waigong_index_arr.length > 0) {
                firstValue = waigong_index_arr.shift();
            } else if (waigong_naigong_index_arr.length > 0) {
                firstValue = waigong_naigong_index_arr.shift();
            } else if (common_index_arr.length > 0) {
                firstValue = common_index_arr.shift();
            }

            set_td_innerHTML(firstValue, waigong_arr[i], "外");
        }

        for(let i = 0; i < neigong_arr.length; i++) {
            let firstValue = -1;
            if (neigong_index_arr.length > 0) {
                firstValue = neigong_index_arr.shift();
            } else if (waigong_naigong_index_arr.length > 0) {
                firstValue = waigong_naigong_index_arr.shift();
            } else if (common_index_arr.length > 0) {
                firstValue = common_index_arr.shift();
            }

            set_td_innerHTML(firstValue, neigong_arr[i], "内");
        }

        for(let i = 0; i < rou_arr.length; i++) {
            let firstValue = -1;
            if (rou_nai_index_arr.length > 0) {
                firstValue = rou_nai_index_arr.shift();
            } else if (common_index_arr.length > 0) {
                firstValue = common_index_arr.shift();
            }

            set_td_innerHTML(firstValue, rou_arr[i], "肉");
        }

        for(let i = 0; i < nai_arr.length; i++) {
            let firstValue = -1;
            if (rou_nai_index_arr.length > 0) {
                firstValue = rou_nai_index_arr.shift();
            } else if (common_index_arr.length > 0) {
                firstValue = common_index_arr.shift();
            }

            set_td_innerHTML(firstValue, nai_arr[i], "奶");
        }
        
    }

    create_table(data_json)
}

// 获取门派图片文件名，用于设置门派图片
function get_sect_img_file_name(input) {
    switch (input) {
        case '刀宗':
        case '孤锋诀': 
            return '孤锋诀'
        case '北天药宗':
        case "药宗":
        case "药宗输出":
        case "药宗dps": 
        case '无方':
            return '无方'
        case '衍天宗':
        case "衍天":
        case "太玄": 
        case '太玄经': 
            return '太玄经'
        case '凌雪阁':
        case "隐龙":
        case "凌雪": 
        case "隐龙诀": 
            return '隐龙诀'
        case '蓬莱':
        case "凌海":
        case "伞爹": 
            return '凌海诀'
        case '霸刀':
        case "北傲":
        case "刀爹": 
        case "北傲诀": 
            return '北傲诀'
        case '长歌':
        case "长歌输出":
        case "长歌dps": 
        case "莫问": 
            return '莫问'
        case '苍云':
        case "分山": 
        case "苍云输出": 
        case "苍云dps": 
        case "分山劲": 
            return '分山劲'
        case '丐帮': 
        case "笑尘":
        case "丐丐":
        case "要饭的": 
        case "笑尘诀": 
            return '笑尘诀'
        case '明教':
        case "焚影": 
        case "明教dps": 
        case "明教输出": 
        case "明教":
        case "喵喵": 
        case "焚影圣诀": 
            return '焚影圣诀'
        case '五毒': 
        case "读经":
        case "五毒dps":
        case "五毒输出":
        case "五毒": 
        case "毒经": 
            return '毒经'
        case '天策':
        case "傲雪": 
        case "傲血":
        case "天策dps": 
        case "天策输出": 
        case "哈士奇": 
        case "傲血战意": 
            return '傲血战意'
        case '纯阳':
        case "太虚": 
        case "剑纯": 
        case "渣男": 
        case "太虚剑意": 
            return '太虚剑意'
        case '少林': 
        case "易筋": 
        case "和尚dps": 
        case "和尚输出": 
        case "大师dps": 
        case "大师输出": 
        case "少林dps": 
        case "少林输出": 
        case "和尚": 
        case "少林": 
        case "光头": 
        case "易筋经": 
            return '易筋经'
        case '万花':
        case "花间": 
        case "万花dps": 
        case "万花输出": 
        case "万花": 
        case "花花": 
        case "花间游": 
            return '花间游'
        case "田螺":
        case "天罗": 
        case "天罗诡道": 
            return "天罗诡道"
        case "离经": 
        case "离经": 
        case "奶花": 
        case "花奶": 
        case "离经易道": 
            return "离经易道"
        case "长歌治疗":
        case "长歌奶": 
        case "歌奶": 
        case "奶歌": 
        case "相知": 
            return "相知"
        case "铁骨": 
        case "苍云T": 
        case "苍云t":
        case "铁王八": 
        case "铁骨衣": 
            return "铁骨衣"
        case "明尊": 
        case "明教T": 
        case "明教t": 
        case "喵T": 
        case "喵t": 
        case "明尊琉璃体": 
            return "明尊琉璃体"
        case '唐门': 
        case "惊羽":
        case "鲸鱼": 
        case "惊羽诀": 
            return "惊羽诀"
        case "补天": 
        case "奶毒":
        case "毒奶": 
        case "补天诀": 
            return "补天诀"
        case "问水诀": 
        case "藏剑": 
        case "黄鸡": 
        case "山居": 
        case "问水": 
        case "鸡哥":
        case "风车侠": 
        case "山居剑意": 
            return "山居剑意"
        case "铁牢": 
        case "策T": 
        case "策t": 
        case "天策T": 
        case "天策t": 
        case "铁牢律": 
            return "铁牢律"
        case "紫霞":
        case "气纯": 
        case "紫霞功": 
            return "紫霞功"
        case "洗髓": 
        case "和尚T": 
        case "和尚t": 
        case "大师t": 
        case "大师T": 
        case "少林t": 
        case "少林T": 
        case "洗髓经": 
            return "洗髓经"
        case "冰心": 
        case "冰秀": 
        case "七秀dps": 
        case "七秀输出": 
        case "七秀": 
        case "秀秀": 
        case "冰心诀": 
            return "冰心诀"
        case "云裳": 
        case "秀奶": 
        case "奶秀": 
        case "云裳心经": 
            return "云裳心经"
        default:
            return "异常"; // 或者抛出异常等其他处理方式
    }
}

// 判断字符串是否在数组中
function isStringInArray(str, arr) {
    // 使用 includes 方法判断字符串是否在数组中
    if (arr.includes(str)) {
        return true;
    } else {
        return false;
    }
}

// 设置td的内容
function set_td_innerHTML(id, json, job) {
    let str = "";

    console.log("json[\"QQ\"]:" + json["QQ"]);

    if (json["QQ"] == create_user_qq) {
        str = '<div class="td_container">' +
            '<div class="td_div_img"><img src="img/门派/' + get_sect_img_file_name(json["门派"]) + '.png"/>' + '</div>' + 
            // 团长ID的颜色 修改下面的color后面的rgb
            '<div class="td_div_id" style="color: #ff0808">' + json["ID"] + '</div>' +
            '<div class="td_div_qq">' + json["QQ"] + '</div>' +
            '</div>'
    } else if (json["ID"].indexOf("老板") != -1) {
        str = '<div class="td_container">' +
            '<div class="td_div_img"><img src="img/门派/' + get_sect_img_file_name(json["门派"]) + '.png"/>' + '</div>' + 
            // 老板ID的颜色 修改下面的color后面的rgb
            '<div class="td_div_id" style="color: #ff0000">' + json["ID"] + '</div>' +
            '<div class="td_div_qq">' + json["QQ"] + '</div>' +
            '</div>'
    } else if (job == "外"){
        str = '<div class="td_container">' +
            '<div class="td_div_img"><img src="img/门派/' + get_sect_img_file_name(json["门派"]) + '.png"/>' + '</div>' + 
            // 外功ID的颜色 修改下面的color后面的rgb
            '<div class="td_div_id" style="color: #F0E68C">' + json["ID"] + '</div>' +
            '<div class="td_div_qq">' + json["QQ"] + '</div>' +
            '</div>'
    } else if (job == "内"){
        str = '<div class="td_container">' +
            '<div class="td_div_img"><img src="img/门派/' + get_sect_img_file_name(json["门派"]) + '.png"/>' + '</div>' + 
            // 内功ID的颜色 修改下面的color后面的rgb
            '<div class="td_div_id" style="color: #8A2BE2">' + json["ID"] + '</div>' +
            '<div class="td_div_qq">' + json["QQ"] + '</div>' +
            '</div>'
    } else if (job == "肉"){
        str = '<div class="td_container">' +
            '<div class="td_div_img"><img src="img/门派/' + get_sect_img_file_name(json["门派"]) + '.png"/>' + '</div>' + 
            // 肉ID的颜色 修改下面的color后面的rgb
            '<div class="td_div_id" style="color: #B22222">' + json["ID"] + '</div>' +
            '<div class="td_div_qq">' + json["QQ"] + '</div>' +
            '</div>'
    } else if (job == "奶"){
        str = '<div class="td_container">' +
            '<div class="td_div_img"><img src="img/门派/' + get_sect_img_file_name(json["门派"]) + '.png"/>' + '</div>' + 
            // 奶ID的颜色 修改下面的color后面的rgb
            '<div class="td_div_id" style="color: #FFB6C1">' + json["ID"] + '</div>' +
            '<div class="td_div_qq">' + json["QQ"] + '</div>' +
            '</div>'
    }

    document.getElementById("td_" + id).innerHTML = str;

    document.getElementById("td_" + id).style.background = "rgb(172 217 241)";
}