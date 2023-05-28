// 添加页面数据
function load_data(json_str) {
    let data_json = JSON.parse(json_str);

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
        const th1 = document.createElement('th');
        const th2 = document.createElement('th');
        const th3 = document.createElement('th');
        const th4 = document.createElement('th');
        const th5 = document.createElement('th');
        th1.innerHTML = '团本编号';
        th2.innerHTML = '标题';
        th3.innerHTML = '副本最大人数';
        th4.innerHTML = '创始人QQ';
        th5.innerHTML = '创建时间';
        tr.appendChild(th1);
        tr.appendChild(th2);
        tr.appendChild(th3);
        tr.appendChild(th4);
        tr.appendChild(th5);

        const tbody = document.createElement('tbody');
        table.appendChild(tbody);

        // 遍历 JSON 数据中的键名
        for (let key in data_json) {
            // console.log(key);

            const tr = document.createElement('tr');
            tbody.appendChild(tr);

            const td1 = document.createElement('td');
            const td2 = document.createElement('td');
            const td3 = document.createElement('td');
            const td4 = document.createElement('td');
            const td5 = document.createElement('td');
                
            td1.innerHTML = key;
            td2.innerHTML = data_json[key]["标题"];
            td3.innerHTML = data_json[key]["用户列表"].length + '/' + data_json[key]["副本最大人数"];
            td4.innerHTML = data_json[key]["创始人QQ"];
            td5.innerHTML = data_json[key]["创建时间"];

            td2.style.textAlign = "left";
            td2.style.paddingLeft = "10px";

            tr.appendChild(td1);
            tr.appendChild(td2);
            tr.appendChild(td3);
            tr.appendChild(td4);
            tr.appendChild(td5);
        }
    }

    create_table(data_json)
}
