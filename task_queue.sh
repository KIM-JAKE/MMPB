#!/bin/bash

QUEUE_FILE="$HOME/.task_queue"

# 작업 추가
task_add() {
    echo "$1" >> "$QUEUE_FILE"
    echo "작업이 추가되었습니다: $1"
}

# 작업 목록 조회
task_list() {
    if [[ ! -f "$QUEUE_FILE" || ! -s "$QUEUE_FILE" ]]; then
        echo "작업 큐가 비어 있습니다."
    else
        nl -w2 -s": " "$QUEUE_FILE"
    fi
}

# 작업 실행
task_run() {
    if [[ ! -f "$QUEUE_FILE" || ! -s "$QUEUE_FILE" ]]; then
        echo "작업 큐가 비어 있습니다."
        return
    fi
    while IFS= read -r command; do
        echo "실행 중: $command"
        eval "$command"
    done < "$QUEUE_FILE"
    > "$QUEUE_FILE"  # 실행 후 큐 초기화
    echo "모든 작업이 실행되었습니다."
}

# 작업 삭제
task_remove() {
    if [[ ! -f "$QUEUE_FILE" || ! -s "$QUEUE_FILE" ]]; then
        echo "작업 큐가 비어 있습니다."
        return
    fi
    sed -i "${1}d" "$QUEUE_FILE"
    echo "작업 #$1 가 삭제되었습니다."
}

# 작업 초기화
task_clear() {
    > "$QUEUE_FILE"
    echo "작업 큐가 초기화되었습니다."
}

# 명령어 처리
case "$1" in
    add) shift; task_add "$*" ;;
    list) task_list ;;
    run) task_run ;;
    remove) shift; task_remove "$1" ;;
    clear) task_clear ;;
    *)
        echo "사용법: $0 {add|list|run|remove|clear} [args]"
        exit 1
        ;;
esac
